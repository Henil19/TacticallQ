import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from config import GOAL_X, GOAL_Y, PITCH_LENGTH, PITCH_WIDTH

class AnalyticsEngine:
    """
    Core statistical analytics engine computing Expected Goals (xG), Expected Assists (xA),
    tactical pitch average positions, pass networks, cumulative xG timelines, key pass vectors,
    and defensive turnover disruption hubs.
    """

    @staticmethod
    def calculate_xg_from_geometry(x: float, y: float, body_part: str = "Right Foot", play_pattern: str = "Regular Play") -> float:
        """Computes spatial Expected Goals (xG) based on Euclidean distance and goal angle."""
        if x is None or y is None:
            return 0.05

        dx = GOAL_X - x
        dy = abs(GOAL_Y - y)
        dist = np.sqrt(dx**2 + dy**2)
        
        if dist == 0:
            return 0.95

        y_post1 = 36.0
        y_post2 = 44.0
        
        vec1 = np.array([GOAL_X - x, y_post1 - y])
        vec2 = np.array([GOAL_X - x, y_post2 - y])
        
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            angle = np.pi
        else:
            cos_angle = np.clip(np.dot(vec1, vec2) / (norm1 * norm2), -1.0, 1.0)
            angle = np.arccos(cos_angle)

        logit = 0.85 * angle - 0.12 * dist - 0.5
        
        if body_part == "Head":
            logit -= 0.6
        elif body_part in ["Left Foot", "Right Foot"]:
            logit += 0.2
            
        if play_pattern == "Set Piece":
            logit -= 0.3

        xg = 1.0 / (1.0 + np.exp(-logit))
        return float(np.clip(xg, 0.01, 0.96))

    def compute_match_xg_summary(self, events_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates total team xG, shot counts, and average shot quality."""
        shots = events_df[events_df["type"] == "Shot"].copy()
        if shots.empty:
            return {}
            
        if "xg" not in shots.columns or shots["xg"].isnull().any():
            shots["xg"] = shots.apply(
                lambda r: self.calculate_xg_from_geometry(
                    r.get("start_x"), r.get("start_y"), r.get("body_part", "Right Foot"), r.get("play_pattern", "Regular Play")
                ), axis=1
            )

        summary = {}
        teams = shots["team"].dropna().unique()
        for team in teams:
            team_shots = shots[shots["team"] == team]
            total_xg = float(team_shots["xg"].fillna(0.0).sum())
            total_shots = len(team_shots)
            goals = len(team_shots[team_shots["shot_outcome"] == "Goal"])
            avg_xg_per_shot = total_xg / total_shots if total_shots > 0 else 0.0

            summary[team] = {
                "total_xg": round(total_xg, 2),
                "total_shots": total_shots,
                "goals": goals,
                "avg_shot_quality": round(avg_xg_per_shot, 3)
            }

        return summary

    def compute_cumulative_xg_timeline(self, events_df: pd.DataFrame) -> Dict[str, Any]:
        """Computes minute-by-minute cumulative xG trajectories and goal markers."""
        shots = events_df[events_df["type"] == "Shot"].copy()
        if shots.empty:
            return {}

        if "xg" not in shots.columns or shots["xg"].isnull().any():
            shots["xg"] = shots.apply(
                lambda r: self.calculate_xg_from_geometry(r.get("start_x"), r.get("start_y")), axis=1
            )

        shots = shots.sort_values(by=["minute", "second"])
        teams = shots["team"].dropna().unique()
        
        result = {}
        for team in teams:
            t_shots = shots[shots["team"] == team]
            minutes = [0]
            cum_xg = [0.0]
            curr_val = 0.0
            goals = []

            for idx, r in t_shots.iterrows():
                m = int(r["minute"])
                val = float(r.get("xg", 0.05) or 0.05)
                curr_val += val
                minutes.append(m)
                cum_xg.append(round(curr_val, 2))
                
                if r.get("shot_outcome") == "Goal":
                    goals.append({
                        "minute": m,
                        "player": r.get("player", "Player"),
                        "xg": round(val, 2),
                        "cum_xg": round(curr_val, 2)
                    })

            if minutes[-1] < 90:
                minutes.append(90)
                cum_xg.append(cum_xg[-1])

            result[team] = {
                "minutes": minutes,
                "cum_xg": cum_xg,
                "goals": goals
            }

        return result

    def compute_key_passes_and_xa(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts Key Passes (passes leading directly to shots) and assigns Expected Assists (xA).
        """
        if events_df.empty:
            return pd.DataFrame()

        passes = events_df[events_df["type"] == "Pass"].copy()
        shots = events_df[events_df["type"] == "Shot"].copy()

        if passes.empty or shots.empty:
            return pd.DataFrame()

        key_passes = []
        for idx, shot in shots.iterrows():
            s_team = shot.get("team")
            s_min = shot.get("minute", 0)
            s_xg = float(shot.get("xg", 0.1) or 0.1)
            
            # Find pass by same team in same or preceding minute
            pred_passes = passes[
                (passes["team"] == s_team) & 
                (passes["minute"] <= s_min) & 
                (passes["minute"] >= max(0, s_min - 1))
            ]

            if not pred_passes.empty:
                last_pass = pred_passes.iloc[-1]
                key_passes.append({
                    "team": s_team,
                    "passer": last_pass.get("player", "Unknown Passer"),
                    "recipient": last_pass.get("pass_recipient", "Shooter"),
                    "start_x": last_pass.get("start_x"),
                    "start_y": last_pass.get("start_y"),
                    "end_x": last_pass.get("end_x"),
                    "end_y": last_pass.get("end_y"),
                    "xa": round(s_xg, 2),
                    "shot_outcome": shot.get("shot_outcome", "Saved"),
                    "minute": s_min
                })

        return pd.DataFrame(key_passes)

    def compute_defensive_disruptions(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts defensive tackles, interceptions, blocks, and ball recoveries.
        """
        if events_df.empty:
            return pd.DataFrame()

        def_types = ["Interception", "Block", "Duel", "Ball Recovery", "50/50", "Pressure"]
        disruptions = events_df[events_df["type"].isin(def_types)].copy()
        return disruptions

    def compute_player_average_positions(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """Computes mean spatial coordinates (X, Y) for starting XI players."""
        if events_df.empty:
            return pd.DataFrame()

        valid_events = events_df[events_df["start_x"].notnull() & events_df["start_y"].notnull()].copy()
        if valid_events.empty:
            return pd.DataFrame()

        teams = valid_events["team"].dropna().unique()
        home_team = teams[0] if len(teams) > 0 else "Home"

        player_coords = []
        for (team, player), group in valid_events.groupby(["team", "player"]):
            avg_x = group["start_x"].mean()
            avg_y = group["start_y"].mean()
            total_actions = len(group)

            if team != home_team:
                norm_x = 120.0 - avg_x
                norm_y = 80.0 - avg_y
            else:
                norm_x = avg_x
                norm_y = avg_y

            player_coords.append({
                "team": team,
                "player": player,
                "avg_x": round(norm_x, 1),
                "avg_y": round(norm_y, 1),
                "total_actions": total_actions
            })

        return pd.DataFrame(player_coords)

    def compute_pass_network_links(self, events_df: pd.DataFrame, min_passes: int = 1) -> pd.DataFrame:
        """Computes pass connections between players with spatial start and end coordinates."""
        passes = events_df[
            (events_df["type"] == "Pass") & 
            (events_df["pass_recipient"].notnull()) & 
            (events_df["pass_outcome"] == "Complete")
        ].copy()

        if passes.empty:
            return pd.DataFrame()

        connections = passes.groupby(["team", "player", "pass_recipient"]).size().reset_index(name="pass_count")
        connections = connections[connections["pass_count"] >= min_passes]
        return connections

    def compute_field_thirds_pressure(self, events_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Calculates high-press and defensive pressure intensity by field third."""
        pressures = events_df[events_df["type"] == "Pressure"].copy()
        if pressures.empty:
            return {}

        result = {}
        for team in pressures["team"].dropna().unique():
            t_press = pressures[pressures["team"] == team]
            def_third = len(t_press[t_press["start_x"] <= 40])
            mid_third = len(t_press[(t_press["start_x"] > 40) & (t_press["start_x"] <= 80)])
            att_third = len(t_press[t_press["start_x"] > 80])
            total = len(t_press)

            result[team] = {
                "defensive_third": def_third,
                "midfield_third": mid_third,
                "attraction_third": att_third,
                "total_pressures": total,
                "def_pct": round((def_third / total * 100), 1) if total > 0 else 0,
                "mid_pct": round((mid_third / total * 100), 1) if total > 0 else 0,
                "att_pct": round((att_third / total * 100), 1) if total > 0 else 0,
            }

        return result

    def compute_defensive_line_height(self, events_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calculates average defensive line height (mean X coordinate of defensive actions)
        and defensive block compacting width/depth per team.
        """
        if events_df.empty:
            return {}

        def_types = ["Interception", "Block", "Duel", "Ball Recovery", "50/50", "Pressure", "Tackle", "Clearance"]
        def_events = events_df[
            (events_df["type"].isin(def_types)) &
            (events_df["start_x"].notnull()) &
            (events_df["start_y"].notnull())
        ].copy()

        if def_events.empty:
            return {}

        teams = def_events["team"].dropna().unique()
        home_team = teams[0] if len(teams) > 0 else "Home"

        result = {}
        for team in teams:
            t_def = def_events[def_events["team"] == team]
            if t_def.empty:
                continue

            # Standardize orientation so defending goal is at X=0
            if team != home_team:
                norm_x = 120.0 - t_def["start_x"]
            else:
                norm_x = t_def["start_x"]

            mean_height = float(norm_x.mean())
            std_depth = float(norm_x.std()) if len(norm_x) > 1 else 0.0
            width_spread = float(t_def["start_y"].std()) if len(t_def) > 1 else 0.0

            # Classify block type based on height (StatsBomb pitch length = 120 yards)
            if mean_height >= 55.0:
                block_type = "High Press (Aggressive)"
            elif mean_height >= 42.0:
                block_type = "Mid-Block (Balanced)"
            else:
                block_type = "Low-Block (Deep Defense)"

            result[team] = {
                "avg_line_height_yards": round(mean_height, 1),
                "depth_compactness": round(std_depth, 1),
                "width_compactness": round(width_spread, 1),
                "block_type": block_type,
                "total_defensive_actions": len(t_def)
            }

        return result

    def compute_match_momentum_timeline(self, events_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Computes 15-minute rolling match momentum scores based on xG produced,
        shot volume, and high pressure events.
        """
        if events_df.empty:
            return {}

        teams = events_df["team"].dropna().unique()
        if len(teams) == 0:
            return {}

        intervals = [
            ("0-15'", 0, 15),
            ("15-30'", 15, 30),
            ("30-45'", 30, 45),
            ("45-60'", 45, 60),
            ("60-75'", 60, 75),
            ("75-90+'", 75, 120)
        ]

        labels = [intv[0] for intv in intervals]
        timeline = {team: [] for team in teams}

        for label, start_m, end_m in intervals:
            intv_events = events_df[(events_df["minute"] >= start_m) & (events_df["minute"] < end_m)]

            for team in teams:
                t_events = intv_events[intv_events["team"] == team]
                shots = t_events[t_events["type"] == "Shot"]
                pressures = t_events[(t_events["type"] == "Pressure") & (t_events["start_x"] > 40)]

                xg = shots["xg"].sum() if ("xg" in shots.columns and not shots["xg"].isnull().all()) else len(shots) * 0.08
                momentum_score = round((xg * 5.0) + (len(shots) * 0.8) + (len(pressures) * 0.2), 2)
                timeline[team].append(momentum_score)

        return {
            "intervals": labels,
            "momentum": timeline
        }

    def compute_pass_directness_index(self, events_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Calculates pass directness ratio (% of passes moving forward towards opponent goal)
        and average pass distance.
        """
        passes = events_df[
            (events_df["type"] == "Pass") &
            (events_df["start_x"].notnull()) &
            (events_df["end_x"].notnull()) &
            (events_df["pass_outcome"] == "Complete")
        ].copy()

        if passes.empty:
            return {}

        teams = passes["team"].dropna().unique()
        home_team = teams[0] if len(teams) > 0 else "Home"

        result = {}
        for team in teams:
            t_passes = passes[passes["team"] == team]
            total_passes = len(t_passes)
            if total_passes == 0:
                continue

            # Forward passes (dx > 5.0 yards towards attacking end)
            if team == home_team:
                forward_passes = len(t_passes[t_passes["end_x"] - t_passes["start_x"] > 5.0])
            else:
                forward_passes = len(t_passes[t_passes["start_x"] - t_passes["end_x"] > 5.0])

            directness_pct = round((forward_passes / total_passes) * 100, 1)

            # Calculate pass distance
            dx = t_passes["end_x"] - t_passes["start_x"]
            dy = t_passes["end_y"] - t_passes["start_y"]
            avg_dist = float(np.sqrt(dx**2 + dy**2).mean())

            result[team] = {
                "total_completed_passes": total_passes,
                "forward_passes": forward_passes,
                "directness_pct": directness_pct,
                "avg_pass_length_yards": round(avg_dist, 1)
            }

        return result

