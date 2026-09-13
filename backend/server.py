import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

# Add project root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Query, HTTPException, Body
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from modules.data_loader import DataLoader
from modules.analytics_engine import AnalyticsEngine
from modules.ml_clustering import PlayerClusteringModel
from modules.live_search import LiveSearchEngine
from modules.ai_analyst import AITacticalAnalyst

app = FastAPI(
    title="TacticalIQ API",
    description="REST API for UEFA Euro 2024 AI Football Analytics Platform",
    version="2.5.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core engines
data_loader = DataLoader()
analytics_engine = AnalyticsEngine()
ml_clustering_model = PlayerClusteringModel()
live_search_engine = LiveSearchEngine()


class AIReportRequest(BaseModel):
    match_id: int
    api_key: Optional[str] = None


class AIScoutQueryRequest(BaseModel):
    match_id: int
    query: str
    api_key: Optional[str] = None


class CounterStrategyRequest(BaseModel):
    opponent_team: str
    formation: str
    playstyle: str
    key_player: str
    api_key: Optional[str] = None


import math
import numpy as np

def sanitize_obj(obj):
    """Recursively converts NaN, Inf, and numpy types to None/Python primitives for JSON compliance."""
    if obj is None:
        return None
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        val = float(obj)
        if math.isnan(val) or math.isinf(val):
            return None
        return val
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, dict):
        return {k: sanitize_obj(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize_obj(v) for v in obj]
    return obj


def clean_df(df: pd.DataFrame) -> list:
    """Helper to convert pandas DataFrame to JSON-serializable list of dicts with full NaN/Inf sanitization."""
    if df is None or df.empty:
        return []
    records = df.to_dict(orient="records")
    return sanitize_obj(records)


@app.get("/api/matches")
def get_matches(query: Optional[str] = None, stage: Optional[str] = None):
    """Fetches all matches with optional search query and stage filter."""
    matches_df = data_loader.fetch_all_matches()
    if matches_df.empty:
        return {"matches": [], "stages": []}

    all_stages = ["All"] + sorted(matches_df["stage"].dropna().unique().tolist())
    filtered = data_loader.search_matches(query=query or "", stage_filter=stage or "All")

    return sanitize_obj({
        "matches": clean_df(filtered),
        "stages": all_stages
    })


@app.get("/api/matches/{match_id}/telemetry")
def get_match_telemetry(match_id: int):
    """Returns complete aggregated match telemetry including xG summary, defensive line height, pass directness, and timelines."""
    matches_df = data_loader.fetch_all_matches()
    match_rows = matches_df[matches_df["match_id"] == match_id]
    if match_rows.empty:
        raise HTTPException(status_code=404, detail="Match not found")

    match_info = match_rows.iloc[0].to_dict()
    events_df = data_loader.fetch_match_events(match_id)

    xg_summary = analytics_engine.compute_match_xg_summary(events_df)
    cum_xg_timeline = analytics_engine.compute_cumulative_xg_timeline(events_df)
    key_passes = analytics_engine.compute_key_passes_and_xa(events_df)
    field_thirds_pressure = analytics_engine.compute_field_thirds_pressure(events_df)
    defensive_line_height = analytics_engine.compute_defensive_line_height(events_df)
    match_momentum = analytics_engine.compute_match_momentum_timeline(events_df)
    pass_directness = analytics_engine.compute_pass_directness_index(events_df)

    return sanitize_obj({
        "match_info": match_info,
        "xg_summary": xg_summary,
        "cumulative_xg_timeline": cum_xg_timeline,
        "key_passes_count": len(key_passes),
        "key_passes": clean_df(key_passes),
        "field_thirds_pressure": field_thirds_pressure,
        "defensive_line_height": defensive_line_height,
        "match_momentum": match_momentum,
        "pass_directness": pass_directness,
        "total_events": len(events_df)
    })


@app.get("/api/matches/{match_id}/events")
def get_match_events(match_id: int):
    """Returns raw and structured event spatial coordinates for pitch visualizer."""
    events_df = data_loader.fetch_match_events(match_id)
    if events_df.empty:
        return {"events": [], "shots": [], "pass_links": [], "average_positions": [], "disruptions": []}

    shots_df = events_df[events_df["type"] == "Shot"].copy()
    if not shots_df.empty and "xg" not in shots_df.columns:
        shots_df["xg"] = shots_df.apply(
            lambda r: analytics_engine.calculate_xg_from_geometry(r.get("start_x"), r.get("start_y")), axis=1
        )

    avg_pos = analytics_engine.compute_player_average_positions(events_df)
    pass_links = analytics_engine.compute_pass_network_links(events_df, min_passes=1)
    disruptions = analytics_engine.compute_defensive_disruptions(events_df)

    return sanitize_obj({
        "shots": clean_df(shots_df),
        "pass_links": clean_df(pass_links),
        "average_positions": clean_df(avg_pos),
        "disruptions": clean_df(disruptions)
    })


@app.get("/api/matches/{match_id}/player-stats")
def get_player_stats_and_clustering(match_id: int):
    """Returns player stats aggregates and ML K-Means player tactical role clusters."""
    events_df = data_loader.fetch_match_events(match_id)
    player_stats_df = data_loader.get_player_stats_for_events(events_df)

    if player_stats_df.empty:
        return {"players": [], "clusters": []}

    clustered_df = ml_clustering_model.train_and_predict(player_stats_df)
    return sanitize_obj({
        "players": clean_df(player_stats_df),
        "clusters": clean_df(clustered_df)
    })


@app.post("/api/ai/report")
def generate_ai_report(req: AIReportRequest):
    """Generates executive AI tactical match report via Gemini LLM API or domain synthesis fallback."""
    matches_df = data_loader.fetch_all_matches()
    match_rows = matches_df[matches_df["match_id"] == req.match_id]
    if match_rows.empty:
        raise HTTPException(status_code=404, detail="Match not found")

    match_info = match_rows.iloc[0].to_dict()
    events_df = data_loader.fetch_match_events(req.match_id)
    xg_summary = analytics_engine.compute_match_xg_summary(events_df)

    home = match_info.get("home_team", "Home")
    away = match_info.get("away_team", "Away")
    live_context = live_search_engine.search_live_news(f"{home} vs {away} Euro 2024 tactics")

    ai_analyst = AITacticalAnalyst(api_key=req.api_key)
    report = ai_analyst.generate_tactical_match_report(match_info, xg_summary, live_context)

    return sanitize_obj({
        "report": report,
        "live_context": live_context
    })


@app.post("/api/ai/scout")
def run_ai_scout_query(req: AIScoutQueryRequest):
    """Performs live web search and answers custom tactical scouting query."""
    matches_df = data_loader.fetch_all_matches()
    match_rows = matches_df[matches_df["match_id"] == req.match_id]
    match_info = match_rows.iloc[0].to_dict() if not match_rows.empty else {}

    live_results = live_search_engine.search_live_news(req.query, max_results=3)
    ai_analyst = AITacticalAnalyst(api_key=req.api_key)
    answer = ai_analyst.answer_scout_query(req.query, match_info, live_results)

    return sanitize_obj({
        "query": req.query,
        "answer": answer,
        "live_results": live_results
    })


@app.post("/api/ai/counter-strategy")
def simulate_counter_strategy(req: CounterStrategyRequest):
    """Simulates custom AI tactical counter-strategy blueprint against given opponent playstyle."""
    ai_analyst = AITacticalAnalyst(api_key=req.api_key)
    blueprint = ai_analyst.simulate_tactical_counter_strategy(
        req.opponent_team, req.formation, req.playstyle, req.key_player
    )
    return sanitize_obj({
        "blueprint": blueprint
    })


@app.get("/api/leaderboards")
def get_leaderboards():
    """Returns tournament-wide player metrics leaderboards."""
    leaderboards = data_loader.get_tournament_leaderboards()
    cleaned_leaderboards = {}
    for key, df in leaderboards.items():
        cleaned_leaderboards[key] = clean_df(df)
    return sanitize_obj(cleaned_leaderboards)


@app.get("/api/head-to-head")
def get_head_to_head(match_a_id: int, match_b_id: int):
    """Returns comparative telemetry between two selected matches."""
    matches_df = data_loader.fetch_all_matches()
    match_a_row = matches_df[matches_df["match_id"] == match_a_id]
    match_b_row = matches_df[matches_df["match_id"] == match_b_id]

    if match_a_row.empty or match_b_row.empty:
        raise HTTPException(status_code=404, detail="One or both matches not found")

    events_a = data_loader.fetch_match_events(match_a_id)
    events_b = data_loader.fetch_match_events(match_b_id)

    return sanitize_obj({
        "match_a": {
            "info": match_a_row.iloc[0].to_dict(),
            "xg_summary": analytics_engine.compute_match_xg_summary(events_a),
            "defensive_line": analytics_engine.compute_defensive_line_height(events_a),
            "pass_directness": analytics_engine.compute_pass_directness_index(events_a)
        },
        "match_b": {
            "info": match_b_row.iloc[0].to_dict(),
            "xg_summary": analytics_engine.compute_match_xg_summary(events_b),
            "defensive_line": analytics_engine.compute_defensive_line_height(events_b),
            "pass_directness": analytics_engine.compute_pass_directness_index(events_b)
        }
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

