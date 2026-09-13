import sys
import os
import pandas as pd
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def test_full_pipeline():
    print("=== Testing TacticalIQ Advanced Expansion Pipeline ===")
    
    # 1. Test DataLoader Dynamic Matches Fetching & Leaderboards
    from modules.data_loader import DataLoader
    loader = DataLoader()
    matches = loader.fetch_all_matches()
    leaderboards = loader.get_tournament_leaderboards()
    assert not matches.empty, "Matches DataFrame is empty!"
    print(f"[OK] DataLoader web API passed: Fetched index of {len(matches)} UEFA Euro 2024 fixtures.")

    # 2. Test Dynamic Event Stream & Starting XI Position Mapping
    first_match_id = matches["match_id"].iloc[0]
    events = loader.fetch_match_events(first_match_id)
    player_stats = loader.get_player_stats_for_events(events)
    assert not events.empty, "Events DataFrame is empty!"
    assert not player_stats.empty, "Player stats DataFrame is empty!"
    print(f"[OK] Starting XI positions extracted for {len(player_stats)} players.")

    # 3. Test Analytics Engine Cumulative xG, Key Passes xA & Defensive Disruptions
    from modules.analytics_engine import AnalyticsEngine
    analytics = AnalyticsEngine()
    xg_summary = analytics.compute_match_xg_summary(events)
    cum_xg_timeline = analytics.compute_cumulative_xg_timeline(events)
    key_passes = analytics.compute_key_passes_and_xa(events)
    disruptions = analytics.compute_defensive_disruptions(events)
    avg_pos = analytics.compute_player_average_positions(events)
    pass_links = analytics.compute_pass_network_links(events)
    def_line_height = analytics.compute_defensive_line_height(events)
    momentum_data = analytics.compute_match_momentum_timeline(events)
    directness_data = analytics.compute_pass_directness_index(events)

    assert cum_xg_timeline != {}, "Cumulative xG timeline data empty!"
    assert def_line_height != {}, "Defensive line height data empty!"
    assert momentum_data != {}, "Match momentum data empty!"
    assert directness_data != {}, "Pass directness data empty!"
    print(f"[OK] AnalyticsEngine passed: Computed xG summary, key pass xA vectors ({len(key_passes)} key passes), defensive line heights, match momentum, and pass directness.")

    # 4. Test Dynamic Centroid ML Clustering
    from modules.ml_clustering import PlayerClusteringModel
    model = PlayerClusteringModel()
    clustered_df = model.train_and_predict(player_stats)
    assert "tactical_role" in clustered_df.columns, "Tactical role column missing!"
    print(f"[OK] Dynamic Centroid ML Clustering passed: {len(clustered_df)} players dynamically profiled into roles.")

    # 5. Test Live Search Engine
    from modules.live_search import LiveSearchEngine
    searcher = LiveSearchEngine()
    results = searcher.search_live_news("Spain vs England Euro 2024 final tactics")
    assert len(results) > 0, "Live search returned no results!"
    print(f"[OK] LiveSearchEngine passed: Retrieved {len(results)} live web search results.")

    # 6. Test AI Analyst Module
    from modules.ai_analyst import AITacticalAnalyst
    analyst = AITacticalAnalyst()
    report = analyst.generate_tactical_match_report(matches.iloc[0].to_dict(), xg_summary, results)
    blueprint = analyst.simulate_tactical_counter_strategy("England", "5-3-2", "Low Block Counter", "Bellingham")
    assert len(report) > 100, "Match report output too short!"
    assert len(blueprint) > 100, "Counter strategy output too short!"
    print("[OK] AITacticalAnalyst passed: Executive AI match report and counter-strategy blueprint generated cleanly.")

    # 7. Test Visualizer Dual-Goal Pitch, Pass Networks, Key Pass Vectors, Defensive Disruptions & Heatmaps
    from modules.visualization import PitchVisualizer, HAS_MATPLOTLIB
    viz = PitchVisualizer()
    shots = events[events["type"] == "Shot"]
    fig_shot = viz.plot_shot_map(shots, home_team="Spain", away_team="England")
    fig_pass = viz.plot_tactical_pass_network(avg_pos, pass_links)
    fig_timeline = viz.plot_xg_timeline(cum_xg_timeline)
    fig_heatmap = viz.plot_pressure_heatmap(events, team_name="Spain")
    fig_kp = viz.plot_key_pass_vectors(key_passes, team_name="Spain")
    fig_dis = viz.plot_defensive_disruption_map(disruptions, team_name="Spain")
    fig_pca = viz.plot_pca_clusters(clustered_df)
    fig_mom = viz.plot_team_momentum_chart(momentum_data)
    fig_def_line = viz.plot_defensive_line_comparison(def_line_height)

    if len(clustered_df) >= 2:
        fig_radar = viz.plot_player_radar_comparison(clustered_df.iloc[0], clustered_df.iloc[1])
    else:
        fig_radar = None

    if HAS_MATPLOTLIB:
        assert fig_shot is not None, "Shot map figure creation failed!"
        assert fig_pass is not None, "Pass network figure creation failed!"
        assert fig_timeline is not None, "xG timeline figure creation failed!"
        assert fig_heatmap is not None, "Pressure heatmap figure creation failed!"
        assert fig_kp is not None, "Key pass vector figure creation failed!"
        assert fig_dis is not None, "Defensive disruption figure creation failed!"
        assert fig_pca is not None, "PCA plot figure creation failed!"
        assert fig_mom is not None, "Momentum chart figure creation failed!"
        assert fig_def_line is not None, "Defensive line comparison figure creation failed!"
        print("[OK] PitchVisualizer passed: Shot maps, pass networks, xG timeline, momentum charts, defensive line graphics, and radar graphics rendered.")

    print("\nALL ADVANCED EXPANSION PIPELINE TESTS PASSED 100% CLEANLY!")


if __name__ == "__main__":
    test_full_pipeline()
