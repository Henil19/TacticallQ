import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from config import PITCH_LENGTH, PITCH_WIDTH, THEME_COLORS

HAS_MATPLOTLIB = False
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import seaborn as sns
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class PitchVisualizer:
    """
    Renders football pitch diagrams, dual-goal shot maps, tactical pass networks,
    spatial pressure heatmaps, key pass xA vectors, defensive disruption maps,
    boundary-aware cumulative xG timelines, 1v1 player radar comparisons, and ML cluster plots.
    """

    @staticmethod
    def create_pitch(ax=None, bg_color: str = THEME_COLORS["pitch_bg"], line_color: str = THEME_COLORS["pitch_lines"]):
        """Renders a standard 120 x 80 yard football pitch with custom colors."""
        if not HAS_MATPLOTLIB:
            return None, None

        if ax is None:
            fig, ax = plt.subplots(figsize=(10.5, 6.8))

        ax.set_facecolor(bg_color)
        fig = ax.get_figure()
        fig.patch.set_facecolor(bg_color)

        ax.plot([0, 0, PITCH_LENGTH, PITCH_LENGTH, 0], [0, PITCH_WIDTH, PITCH_WIDTH, 0, 0], color=line_color, lw=1.5)
        ax.plot([60, 60], [0, PITCH_WIDTH], color=line_color, lw=1.5)
        
        center_circle = patches.Circle((60, 40), 9.15, color=line_color, fill=False, lw=1.5)
        ax.add_patch(center_circle)
        ax.plot(60, 40, "o", color=line_color, ms=3)

        ax.plot([0, 18, 18, 0], [18, 18, 62, 62], color=line_color, lw=1.5)
        ax.plot([0, 6, 6, 0], [30, 30, 50, 50], color=line_color, lw=1.2)
        ax.plot([0, -2, -2, 0], [36, 36, 44, 44], color=line_color, lw=1.8)

        ax.plot([120, 102, 102, 120], [18, 18, 62, 62], color=line_color, lw=1.5)
        ax.plot([120, 114, 114, 120], [30, 30, 50, 50], color=line_color, lw=1.2)
        ax.plot([120, 122, 122, 120], [36, 36, 44, 44], color=line_color, lw=1.8)

        ax.set_xlim(-5, 125)
        ax.set_ylim(-5, 85)
        ax.axis("off")
        return fig, ax

    def plot_shot_map(
        self,
        shots_df: pd.DataFrame,
        home_team: str = "Home",
        away_team: str = "Away",
        title: str = "Euro 2024 Dual-Goal Shot Quality Map"
    ):
        """Plots shot locations on a full pitch attacking BOTH goals."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = self.create_pitch()

        if shots_df.empty:
            ax.text(60, 40, "No Shot Events Found for Match", color="white", ha="center", fontsize=14)
            return fig

        outcome_colors = {
            "Goal": "#10B981",    # Emerald Green
            "Saved": "#F59E0B",   # Amber
            "Off T": "#EF4444",   # Red
            "Blocked": "#6B7280"  # Gray
        }

        teams = shots_df["team"].dropna().unique()
        if len(teams) > 0:
            home_team = teams[0]
        if len(teams) > 1:
            away_team = teams[1]

        for idx, row in shots_df.iterrows():
            orig_x = row.get("start_x", 100)
            orig_y = row.get("start_y", 40)
            team = row.get("team")
            xg = row.get("xg", 0.1)
            outcome = row.get("shot_outcome", "Saved")
            player = row.get("player", "")

            if team != home_team:
                plot_x = 120.0 - orig_x
                plot_y = 80.0 - orig_y
            else:
                plot_x = orig_x
                plot_y = orig_y

            size = max(50, (xg or 0.05) * 550)
            color = outcome_colors.get(outcome, "#38BDF8")

            ax.scatter(plot_x, plot_y, s=size, color=color, alpha=0.85, edgecolors="white", linewidth=1.2, zorder=4)
            if outcome == "Goal":
                ax.annotate(f"{player} ({xg:.2f})", (plot_x, plot_y + 2.5), color="#F8FAFC", fontsize=9, fontweight="bold", ha="center")

        ax.annotate(f"⚽ {home_team} Attack ➡️", (90, 81), color="#38BDF8", fontsize=11, fontweight="bold", ha="center")
        ax.annotate(f"⬅️ {away_team} Attack ⚽", (30, 81), color="#F43F5E", fontsize=11, fontweight="bold", ha="center")

        for outcome, clr in outcome_colors.items():
            ax.scatter([], [], color=clr, label=outcome, s=70, edgecolors="white")
            
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=4, facecolor=THEME_COLORS["card_bg"], edgecolor=THEME_COLORS["pitch_lines"], labelcolor="white")
        ax.set_title(title, color="white", fontsize=14, pad=15, fontweight="bold")
        return fig

    def plot_key_pass_vectors(self, key_passes_df: pd.DataFrame, team_name: str):
        """Renders Key Passes & Expected Assists (xA) Directional Vector Arrows."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = self.create_pitch()
        t_kp = key_passes_df[key_passes_df["team"] == team_name].copy() if not key_passes_df.empty else pd.DataFrame()

        if t_kp.empty:
            ax.text(60, 40, f"No Key Passes Recorded for {team_name}", color="white", ha="center", fontsize=13)
            return fig

        for idx, row in t_kp.iterrows():
            x1, y1 = row.get("start_x"), row.get("start_y")
            x2, y2 = row.get("end_x"), row.get("end_y")
            xa = row.get("xa", 0.1)
            passer = row.get("passer", "").split()[-1]

            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                dx = x2 - x1
                dy = y2 - y1
                clr = "#10B981" if row.get("shot_outcome") == "Goal" else "#38BDF8"
                lw = min(3.5, 1.0 + xa * 5)

                ax.arrow(x1, y1, dx, dy, color=clr, head_width=1.8, head_length=2.2, length_includes_head=True, lw=lw, alpha=0.85, zorder=4)
                ax.annotate(f"{passer} (xA {xa:.2f})", (x1, y1 + 1.8), color="white", fontsize=8, fontweight="bold", ha="center", zorder=5)

        ax.set_title(f"🎯 {team_name} Key Pass & Expected Assists (xA) Creation Vectors", color="white", fontsize=13, pad=12, fontweight="bold")
        return fig

    def plot_defensive_disruption_map(self, disruptions_df: pd.DataFrame, team_name: str):
        """Renders spatial defensive disruption hubs (tackles, interceptions, recoveries)."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = self.create_pitch()
        t_dis = disruptions_df[disruptions_df["team"] == team_name].copy() if not disruptions_df.empty else pd.DataFrame()

        if t_dis.empty or "start_x" not in t_dis.columns:
            ax.text(60, 40, f"No Defensive Actions Recorded for {team_name}", color="white", ha="center", fontsize=13)
            return fig

        type_colors = {
            "Interception": "#38BDF8",
            "Block": "#A855F7",
            "Duel": "#F59E0B",
            "Ball Recovery": "#10B981",
            "Pressure": "#F43F5E"
        }

        for idx, row in t_dis.iterrows():
            x = row.get("start_x")
            y = row.get("start_y")
            evt_type = row.get("type", "Pressure")
            clr = type_colors.get(evt_type, "#64748B")

            if x is not None and y is not None:
                ax.scatter(x, y, color=clr, s=45, alpha=0.75, edgecolors="white", linewidth=0.6, zorder=4)

        for evt_type, clr in type_colors.items():
            ax.scatter([], [], color=clr, label=evt_type, s=60, edgecolors="white")

        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=5, facecolor=THEME_COLORS["card_bg"], edgecolor=THEME_COLORS["pitch_lines"], labelcolor="white")
        ax.set_title(f"🛡️ {team_name} Defensive Disruption & Turnover Hubs", color="white", fontsize=13, pad=12, fontweight="bold")
        return fig

    def plot_pressure_heatmap(self, events_df: pd.DataFrame, team_name: str):
        """Renders 2D Spatial Pressure Density Heatmap for a team."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = self.create_pitch()
        pressures = events_df[(events_df["type"] == "Pressure") & (events_df["team"] == team_name)].copy()

        if pressures.empty or "start_x" not in pressures.columns:
            ax.text(60, 40, f"No Pressure Events Recorded for {team_name}", color="white", ha="center", fontsize=13)
            return fig

        sns.kdeplot(
            data=pressures,
            x="start_x", y="start_y",
            fill=True,
            cmap="mako",
            alpha=0.6,
            levels=10,
            ax=ax,
            zorder=3
        )

        ax.scatter(pressures["start_x"], pressures["start_y"], color="#F43F5E", s=25, alpha=0.7, edgecolors="white", linewidth=0.5, zorder=4)
        ax.set_title(f"🔥 {team_name} Spatial Defensive Pressure Heatmap", color="white", fontsize=13, pad=12, fontweight="bold")
        return fig

    def plot_tactical_pass_network(
        self,
        avg_pos_df: pd.DataFrame,
        connections_df: pd.DataFrame,
        title: str = "Tactical Pass Network & Average Positional Lineups"
    ):
        """Plots starting player average positions (X, Y) and passing connections across both pitch halves."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = self.create_pitch()

        if avg_pos_df.empty:
            ax.text(60, 40, "No Positional Data Available", color="white", ha="center", fontsize=14)
            return fig

        teams = avg_pos_df["team"].unique()
        team_colors = {teams[0]: "#38BDF8"}
        if len(teams) > 1:
            team_colors[teams[1]] = "#F43F5E"

        if not connections_df.empty:
            pos_dict = avg_pos_df.set_index("player")[["avg_x", "avg_y"]].to_dict("index")
            for idx, row in connections_df.iterrows():
                p1, p2 = row["player"], row["pass_recipient"]
                cnt = row["pass_count"]
                if p1 in pos_dict and p2 in pos_dict:
                    x1, y1 = pos_dict[p1]["avg_x"], pos_dict[p1]["avg_y"]
                    x2, y2 = pos_dict[p2]["avg_x"], pos_dict[p2]["avg_y"]
                    lw = min(4.0, 0.8 + (cnt * 0.4))
                    ax.plot([x1, x2], [y1, y2], color="#94A3B8", alpha=0.45, lw=lw, zorder=2)

        for idx, row in avg_pos_df.iterrows():
            player = row["player"]
            team = row["team"]
            x = row["avg_x"]
            y = row["avg_y"]
            clr = team_colors.get(team, "#10B981")
            
            parts = player.split()
            short_name = parts[-1] if len(parts) > 1 else player

            ax.scatter(x, y, s=240, color=clr, edgecolors="white", linewidth=1.5, zorder=5)
            ax.annotate(short_name, (x, y + 2.2), color="white", fontsize=8, fontweight="bold", ha="center", zorder=6)

        ax.set_title(title, color="white", fontsize=13, pad=12, fontweight="bold")
        return fig

    def plot_xg_timeline(
        self,
        cum_xg_data: Dict[str, Any],
        title: str = "Match Momentum: Cumulative Expected Goals (xG) Over 90 Minutes"
    ):
        """Plots cumulative xG step curves over 90 minutes with boundary-aware goal annotations."""
        if not HAS_MATPLOTLIB or not cum_xg_data:
            return None

        fig, ax = plt.subplots(figsize=(9.8, 5.2))
        fig.patch.set_facecolor(THEME_COLORS["card_bg"])
        ax.set_facecolor(THEME_COLORS["card_bg"])

        global_max_y = 0.5
        global_max_min = 90

        for team, t_data in cum_xg_data.items():
            c_vals = t_data.get("cum_xg", [0.0])
            m_vals = t_data.get("minutes", [90])
            if c_vals:
                global_max_y = max(global_max_y, max(c_vals))
            if m_vals:
                global_max_min = max(global_max_min, max(m_vals))

        colors = ["#38BDF8", "#F43F5E"]

        for idx, (team, t_data) in enumerate(cum_xg_data.items()):
            mins = t_data.get("minutes", [0, 90])
            cum_xg = t_data.get("cum_xg", [0.0, 0.0])
            clr = colors[idx % len(colors)]

            ax.step(mins, cum_xg, where="post", color=clr, label=f"{team} xG", lw=2.5)

            for g in t_data.get("goals", []):
                gm = g["minute"]
                g_xg = g["cum_xg"]
                p_name = g["player"].split()[-1] if g.get("player") else "Goal"

                ax.plot(gm, g_xg, "o", color="#10B981", ms=10, mec="white", mew=1.5, zorder=5)

                if gm > 75:
                    ha = "right"
                    x_annot = gm - 1.5
                elif gm < 15:
                    ha = "left"
                    x_annot = gm + 1.5
                else:
                    ha = "center"
                    x_annot = gm

                if g_xg > (global_max_y * 0.72):
                    va = "top"
                    y_annot = g_xg - (global_max_y * 0.08)
                else:
                    va = "bottom"
                    y_annot = g_xg + (global_max_y * 0.06)

                ax.annotate(
                    f"Goal: {p_name} ({gm}')",
                    (x_annot, y_annot),
                    color="#F8FAFC",
                    fontsize=8,
                    fontweight="bold",
                    ha=ha,
                    va=va,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=THEME_COLORS["card_bg"], edgecolor=clr, alpha=0.85),
                    zorder=6
                )

        ax.set_ylim(-0.05, global_max_y * 1.35)
        ax.set_xlim(-3, max(95, global_max_min + 5))

        ax.set_xlabel("Match Minute", color="#94A3B8")
        ax.set_ylabel("Cumulative Expected Goals (xG)", color="#94A3B8")
        ax.set_title(title, color="white", fontsize=12, fontweight="bold", pad=12)
        ax.tick_params(colors="white")
        ax.grid(True, color="#334155", linestyle="--", alpha=0.5)
        ax.legend(loc="upper left", facecolor=THEME_COLORS["card_bg"], labelcolor="white", edgecolor=THEME_COLORS["pitch_lines"])

        plt.tight_layout()
        return fig

    def plot_player_radar_comparison(self, player1_row: pd.Series, player2_row: pd.Series):
        """Renders 6-axis Polar Radar Chart comparing 2 selected players."""
        if not HAS_MATPLOTLIB:
            return None

        categories = ["xG Created", "Passes", "Pass Acc %", "Pressures", "Blocks", "Pitch Depth"]
        N = len(categories)

        def extract_metrics(row):
            return [
                min(100, float(row.get("total_xg", 0)) * 120),
                min(100, float(row.get("passes_completed", 0)) * 2.2),
                float(row.get("pass_completion_pct", 75)),
                min(100, float(row.get("pressures", 0)) * 10),
                min(100, float(row.get("blocks", 0)) * 25),
                min(100, (float(row.get("avg_x", 60)) / 120.0) * 100)
            ]

        values1 = extract_metrics(player1_row)
        values2 = extract_metrics(player2_row)

        values1 += values1[:1]
        values2 += values2[:1]

        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6.5, 5.5), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor(THEME_COLORS["card_bg"])
        ax.set_facecolor(THEME_COLORS["card_bg"])

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        plt.xticks(angles[:-1], categories, color="#94A3B8", size=9)
        ax.set_rlabel_position(0)
        plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="#64748B", size=7)
        plt.ylim(0, 100)

        p1_name = player1_row.get("player", "Player 1")
        p2_name = player2_row.get("player", "Player 2")

        ax.plot(angles, values1, linewidth=2, linestyle='solid', label=p1_name, color="#38BDF8")
        ax.fill(angles, values1, color="#38BDF8", alpha=0.25)

        ax.plot(angles, values2, linewidth=2, linestyle='solid', label=p2_name, color="#F43F5E")
        ax.fill(angles, values2, color="#F43F5E", alpha=0.25)

        ax.set_title(f"1v1 Tactical Profile Radar: {p1_name} vs {p2_name}", color="white", fontsize=11, fontweight="bold", pad=15)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), facecolor=THEME_COLORS["card_bg"], labelcolor="white", edgecolor=THEME_COLORS["pitch_lines"])

        plt.tight_layout()
        return fig

    def plot_pca_clusters(self, clustered_df: pd.DataFrame):
        """Plots ML player tactical role clusters in 2D PCA space."""
        if not HAS_MATPLOTLIB:
            return None

        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor(THEME_COLORS["card_bg"])
        ax.set_facecolor(THEME_COLORS["card_bg"])

        n_roles = clustered_df["tactical_role"].nunique()
        palette = ["#38BDF8", "#F43F5E", "#10B981", "#A855F7", "#EAB308", "#EC4899", "#6366F1", "#14B8A6"]
        
        sns.scatterplot(
            data=clustered_df,
            x="pca_x", y="pca_y",
            hue="tactical_role",
            palette=palette[:n_roles] if n_roles <= len(palette) else None,
            s=130,
            ax=ax,
            edgecolor="white",
            linewidth=1.2
        )

        for idx, row in clustered_df.iterrows():
            parts = row["player"].split()
            short_name = parts[-1] if len(parts) > 1 else row["player"]
            ax.annotate(
                short_name, (row["pca_x"] + 0.04, row["pca_y"] + 0.04),
                color="white", fontsize=8, alpha=0.9
            )

        ax.set_title("ML Player Tactical Role Clusters (PCA Reduction)", color="white", fontsize=12, fontweight="bold", pad=10)
        ax.set_xlabel("Principal Component 1 (Creation / Passing Volume)", color="white")
        ax.set_ylabel("Principal Component 2 (Defensive / Pressing Intensity)", color="white")
        ax.tick_params(colors="white")
        ax.legend(facecolor=THEME_COLORS["card_bg"], labelcolor="white", edgecolor=THEME_COLORS["pitch_lines"])

        plt.tight_layout()
        return fig

    def plot_team_momentum_chart(self, momentum_data: Dict[str, Any]):
        """Renders 15-minute rolling match momentum flow chart."""
        if not HAS_MATPLOTLIB or not momentum_data or "intervals" not in momentum_data:
            return None

        intervals = momentum_data["intervals"]
        momentum = momentum_data.get("momentum", {})
        if not momentum:
            return None

        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor(THEME_COLORS["card_bg"])
        ax.set_facecolor(THEME_COLORS["card_bg"])

        colors = ["#38BDF8", "#F43F5E", "#10B981", "#A855F7"]
        x_indices = np.arange(len(intervals))

        for idx, (team, scores) in enumerate(momentum.items()):
            color = colors[idx % len(colors)]
            ax.plot(x_indices, scores, label=team, color=color, linewidth=2.5, marker="o", markersize=6)
            ax.fill_between(x_indices, 0, scores, color=color, alpha=0.15)

        ax.set_title("Match Tactical Momentum Flow (15-Min Intervals)", color="white", fontsize=12, fontweight="bold", pad=10)
        ax.set_xticks(x_indices)
        ax.set_xticklabels(intervals, color="#94A3B8")
        ax.set_ylabel("Momentum Dominance Score", color="#94A3B8")
        ax.tick_params(colors="#94A3B8")
        ax.grid(True, linestyle="--", alpha=0.2, color="#334155")
        ax.legend(facecolor=THEME_COLORS["card_bg"], labelcolor="white", edgecolor=THEME_COLORS["pitch_lines"])

        plt.tight_layout()
        return fig

    def plot_defensive_line_comparison(self, def_line_data: Dict[str, Dict[str, float]]):
        """Renders team defensive block positioning on pitch graphic."""
        if not HAS_MATPLOTLIB or not def_line_data:
            return None

        fig, ax = self.create_pitch()
        colors = ["#38BDF8", "#F43F5E", "#10B981"]
        teams = list(def_line_data.keys())

        for idx, team in enumerate(teams):
            info = def_line_data[team]
            h = info.get("avg_line_height_yards", 45.0)
            block = info.get("block_type", "Mid-Block")
            color = colors[idx % len(colors)]

            # Convert orientation for display
            if idx == 0:
                line_x = h
                ha_align = "left"
                text_x = h + 2.0
            else:
                line_x = 120.0 - h
                ha_align = "right"
                text_x = (120.0 - h) - 2.0

            ax.axvline(x=line_x, color=color, linestyle="--", linewidth=2.5, label=f"{team} Defensive Line ({h} yds)")
            ax.axvspan(
                line_x - 5 if idx == 0 else line_x,
                line_x if idx == 0 else line_x + 5,
                color=color, alpha=0.12
            )

            ax.text(
                text_x, 75 - (idx * 10),
                f"{team}\nLine: {h} yds | {block}",
                color=color, fontsize=10, fontweight="bold", ha=ha_align,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=THEME_COLORS["card_bg"], edgecolor=color, alpha=0.9)
            )

        ax.set_title("Team Defensive Line Height & Pressing Block Depth", color="white", fontsize=12, fontweight="bold", pad=12)
        ax.legend(loc="lower center", facecolor=THEME_COLORS["card_bg"], labelcolor="white", edgecolor=THEME_COLORS["pitch_lines"])
        plt.tight_layout()
        return fig

