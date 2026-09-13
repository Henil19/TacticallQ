import json
import urllib.request
import urllib.error
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import SAMPLE_MATCHES_FILE, SAMPLE_EVENTS_FILE, DATA_DIR

STATSBOMB_MATCHES_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/55/282.json"
STATSBOMB_EVENTS_URL_TEMPLATE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
CACHE_DIR = DATA_DIR / "cache"

class DataLoader:
    """
    Handles local and remote web data ingestion from StatsBomb Open Data API.
    Extracts official Starting XI tactical lineup positions and aggregates tournament leaderboards.
    """
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.matches_df: Optional[pd.DataFrame] = None
        self.current_events_df: Optional[pd.DataFrame] = None
        self.current_match_id: Optional[int] = None
        self.current_player_positions: Dict[str, str] = {}

    def fetch_all_matches(self) -> pd.DataFrame:
        """Fetches all 51 UEFA Euro 2024 matches from StatsBomb Open Data API or local cache."""
        cache_file = CACHE_DIR / "euro2024_all_matches.json"
        
        data = None
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = None

        if not data:
            try:
                req = urllib.request.Request(STATSBOMB_MATCHES_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw_json = resp.read().decode("utf-8")
                    data = json.loads(raw_json)
                    with open(cache_file, "w", encoding="utf-8") as f:
                        f.write(raw_json)
            except Exception:
                if Path(SAMPLE_MATCHES_FILE).exists():
                    with open(SAMPLE_MATCHES_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = []

        parsed_matches = []
        for m in data:
            match_id = m.get("match_id")
            home_team = m.get("home_team", {}).get("home_team_name") or m.get("home_team")
            away_team = m.get("away_team", {}).get("away_team_name") or m.get("away_team")
            home_score = m.get("home_score")
            away_score = m.get("away_score")
            match_date = m.get("match_date")
            stage = m.get("competition_stage", {}).get("name") if isinstance(m.get("competition_stage"), dict) else m.get("stage", "Euro 2024")
            stadium = m.get("stadium", {}).get("name", "Euro 2024 Venue") if isinstance(m.get("stadium"), dict) else m.get("stadium", "Euro 2024 Venue")

            parsed_matches.append({
                "match_id": match_id,
                "match_date": match_date,
                "stage": stage,
                "home_team": home_team,
                "away_team": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "stadium": stadium,
                "display_label": f"{stage}: {home_team} {home_score} - {away_score} {away_team} ({match_date})"
            })

        self.matches_df = pd.DataFrame(parsed_matches)
        return self.matches_df

    def fetch_match_events(self, match_id: int) -> pd.DataFrame:
        """Dynamically fetches event streams and parses official Starting XI tactical lineup positions."""
        cache_file = CACHE_DIR / f"events_{match_id}.json"
        
        events_raw = None
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    events_raw = json.load(f)
            except Exception:
                events_raw = None

        if not events_raw:
            url = STATSBOMB_EVENTS_URL_TEMPLATE.format(match_id=match_id)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    raw_json = resp.read().decode("utf-8")
                    events_raw = json.loads(raw_json)
                    with open(cache_file, "w", encoding="utf-8") as f:
                        f.write(raw_json)
            except Exception:
                if Path(SAMPLE_EVENTS_FILE).exists():
                    with open(SAMPLE_EVENTS_FILE, "r", encoding="utf-8") as f:
                        events_raw = json.load(f)
                else:
                    events_raw = []

        player_positions: Dict[str, str] = {}
        for evt in events_raw:
            type_obj = evt.get("type", {})
            type_name = type_obj.get("name") if isinstance(type_obj, dict) else type_obj

            if type_name == "Starting XI":
                tactical_lineup = evt.get("tactical_lineup", {}).get("lineup", [])
                for item in tactical_lineup:
                    p_name = item.get("player", {}).get("name")
                    pos_name = item.get("position", {}).get("name")
                    if p_name and pos_name:
                        player_positions[p_name] = pos_name

            if type_name == "Substitution":
                p_name = evt.get("substitution", {}).get("replacement", {}).get("name")
                pos_name = evt.get("position", {}).get("name")
                if p_name and pos_name:
                    player_positions[p_name] = pos_name

        self.current_player_positions = player_positions

        parsed_events = []
        for idx, evt in enumerate(events_raw):
            type_obj = evt.get("type", {})
            evt_type = type_obj.get("name") if isinstance(type_obj, dict) else type_obj
            
            team_obj = evt.get("team", {})
            team = team_obj.get("name") if isinstance(team_obj, dict) else team_obj
            
            player_obj = evt.get("player", {})
            player = player_obj.get("name") if isinstance(player_obj, dict) else player_obj

            pos_obj = evt.get("position", {})
            evt_pos = pos_obj.get("name") if isinstance(pos_obj, dict) else evt.get("position_name")
            official_pos = player_positions.get(player) or evt_pos or "Field Player"
            
            location = evt.get("location")
            
            pass_info = evt.get("pass", {})
            pass_end_loc = pass_info.get("end_location") if pass_info else evt.get("pass_end_location")
            pass_outcome = pass_info.get("outcome", {}).get("name", "Complete") if isinstance(pass_info.get("outcome"), dict) else evt.get("pass_outcome", "Complete")
            pass_recipient = pass_info.get("recipient", {}).get("name") if isinstance(pass_info.get("recipient"), dict) else evt.get("pass_recipient")

            shot_info = evt.get("shot", {})
            shot_outcome = shot_info.get("outcome", {}).get("name") if isinstance(shot_info.get("outcome"), dict) else evt.get("shot_outcome")
            shot_xg = shot_info.get("statsbomb_xg") if shot_info else evt.get("xg")
            body_part = shot_info.get("body_part", {}).get("name") if isinstance(shot_info.get("body_part"), dict) else evt.get("body_part", "Right Foot")
            play_pattern = evt.get("play_pattern", {}).get("name") if isinstance(evt.get("play_pattern"), dict) else evt.get("play_pattern", "Regular Play")

            start_x = location[0] if isinstance(location, list) and len(location) >= 2 else None
            start_y = location[1] if isinstance(location, list) and len(location) >= 2 else None
            end_x = pass_end_loc[0] if isinstance(pass_end_loc, list) and len(pass_end_loc) >= 2 else None
            end_y = pass_end_loc[1] if isinstance(pass_end_loc, list) and len(pass_end_loc) >= 2 else None

            parsed_events.append({
                "id": evt.get("id", f"evt_{idx}"),
                "minute": evt.get("minute", 0),
                "second": evt.get("second", 0),
                "period": evt.get("period", 1),
                "team": team,
                "player": player,
                "official_position": official_pos,
                "type": evt_type,
                "location": location,
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y,
                "pass_outcome": pass_outcome,
                "pass_recipient": pass_recipient,
                "shot_outcome": shot_outcome,
                "xg": shot_xg,
                "body_part": body_part,
                "play_pattern": play_pattern
            })

        self.current_events_df = pd.DataFrame(parsed_events)
        self.current_match_id = match_id
        return self.current_events_df

    def search_matches(self, query: str = "", stage_filter: str = "All") -> pd.DataFrame:
        """Helper to search and filter matches by team name or competition stage."""
        if self.matches_df is None or self.matches_df.empty:
            self.fetch_all_matches()
            
        df = self.matches_df.copy()
        if stage_filter != "All":
            df = df[df["stage"] == stage_filter]
            
        if query and query.strip():
            q = query.strip().lower()

            df = df[
                df["home_team"].str.lower().str.contains(q, na=False) |
                df["away_team"].str.lower().str.contains(q, na=False) |
                df["stage"].str.lower().str.contains(q, na=False)
            ]
            
        return df

    def get_player_stats_for_events(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregates player statistics including official Starting XI positions."""
        if events_df.empty:
            return pd.DataFrame()

        valid_events = events_df[events_df["player"].notnull()].copy()
        if valid_events.empty:
            return pd.DataFrame()

        players = valid_events["player"].unique()
        stats_list = []

        for player in players:
            p_df = valid_events[valid_events["player"] == player]
            team = p_df["team"].iloc[0] if len(p_df) > 0 else "Unknown"

            official_pos = self.current_player_positions.get(player)
            if not official_pos:
                positions = p_df["official_position"].dropna()
                positions = positions[positions != "Field Player"]
                official_pos = positions.iloc[0] if not positions.empty else "Field Player"

            avg_x = p_df["start_x"].dropna().mean() if not p_df["start_x"].dropna().empty else 60.0
            avg_y = p_df["start_y"].dropna().mean() if not p_df["start_y"].dropna().empty else 40.0

            passes = p_df[p_df["type"] == "Pass"]
            passes_completed = len(passes[passes["pass_outcome"] == "Complete"])
            passes_attempted = len(passes)

            shots = p_df[p_df["type"] == "Shot"]
            total_xg = shots["xg"].fillna(0.0).sum() if "xg" in shots.columns else 0.0
            goals = len(shots[shots["shot_outcome"] == "Goal"])

            pressures = len(p_df[p_df["type"] == "Pressure"])
            blocks = len(p_df[p_df["type"] == "Block"])

            stats_list.append({
                "player": player,
                "team": team,
                "official_position": official_pos,
                "avg_x": round(float(avg_x), 1),
                "avg_y": round(float(avg_y), 1),
                "passes_attempted": passes_attempted,
                "passes_completed": passes_completed,
                "pass_completion_pct": round((passes_completed / passes_attempted * 100), 1) if passes_attempted > 0 else 0.0,
                "shots": len(shots),
                "goals": goals,
                "total_xg": round(float(total_xg), 2),
                "pressures": pressures,
                "blocks": blocks
            })

        return pd.DataFrame(stats_list)

    def get_tournament_leaderboards(self) -> Dict[str, pd.DataFrame]:
        """Aggregates player metrics across all cached Euro 2024 event streams."""
        all_stats = []
        cached_event_files = list(CACHE_DIR.glob("events_*.json"))

        if not cached_event_files and Path(SAMPLE_EVENTS_FILE).exists():
            cached_event_files = [SAMPLE_EVENTS_FILE]

        for ef in cached_event_files[:10]: # Process cached match files
            try:
                with open(ef, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                
                # Simple parsing for leaderboard aggregation
                for evt in raw_data:
                    p_name = evt.get("player", {}).get("name") if isinstance(evt.get("player"), dict) else evt.get("player")
                    t_name = evt.get("team", {}).get("name") if isinstance(evt.get("team"), dict) else evt.get("team")
                    type_name = evt.get("type", {}).get("name") if isinstance(evt.get("type"), dict) else evt.get("type")
                    
                    if p_name and t_name:
                        xg_val = evt.get("shot", {}).get("statsbomb_xg", 0.0) if type_name == "Shot" else 0.0
                        is_goal = 1 if type_name == "Shot" and (evt.get("shot", {}).get("outcome", {}).get("name") == "Goal" or evt.get("shot_outcome") == "Goal") else 0
                        is_pass_comp = 1 if type_name == "Pass" and (evt.get("pass", {}).get("outcome", {}).get("name", "Complete") == "Complete" or evt.get("pass_outcome") == "Complete") else 0
                        is_press = 1 if type_name == "Pressure" else 0

                        all_stats.append({
                            "player": p_name,
                            "team": t_name,
                            "xg": xg_val or 0.0,
                            "goals": is_goal,
                            "passes": is_pass_comp,
                            "pressures": is_press
                        })
            except Exception:
                continue

        if not all_stats:
            return {}

        df_all = pd.DataFrame(all_stats)
        agg_df = df_all.groupby(["player", "team"]).agg({
            "xg": "sum",
            "goals": "sum",
            "passes": "sum",
            "pressures": "sum"
        }).reset_index()

        agg_df["xg"] = agg_df["xg"].round(2)

        return {
            "top_xg": agg_df.sort_values(by="xg", ascending=False).head(10),
            "top_goals": agg_df.sort_values(by="goals", ascending=False).head(10),
            "top_passes": agg_df.sort_values(by="passes", ascending=False).head(10),
            "top_pressures": agg_df.sort_values(by="pressures", ascending=False).head(10)
        }

if __name__ == "__main__":
    loader = DataLoader()
    matches = loader.fetch_all_matches()
    print("Leaderboards:", loader.get_tournament_leaderboards())
