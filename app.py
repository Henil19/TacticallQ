import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import os

from config import THEME_COLORS
from modules.data_loader import DataLoader
from modules.live_search import LiveSearchEngine
from modules.analytics_engine import AnalyticsEngine
from modules.ml_clustering import PlayerClusteringModel
from modules.ai_analyst import AITacticalAnalyst
from modules.visualization import PitchVisualizer
from modules.ui_components import (
    render_custom_css,
    render_top_header,
    render_bottom_footer,
    render_overview_tab,
    render_spatial_analytics_tab,
    render_ml_clustering_tab,
    render_ai_scout_tab,
    render_tournament_leaderboards_tab,
    render_head_to_head_tab
)

# ---------------------------------------------------------
# Page Configuration & Custom CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="TacticalIQ | UEFA Euro 2024 AI Analytics Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern CSS styling, glassmorphic cards, button hover/click micro-interactions, and hide Streamlit default chrome
render_custom_css()

# ---------------------------------------------------------
# Core Services & Data Loading
# ---------------------------------------------------------
@st.cache_resource
def get_services():
    return (
        DataLoader(),
        AnalyticsEngine(),
        PitchVisualizer(),
        LiveSearchEngine()
    )

loader, analytics_engine, visualizer, live_search = get_services()

@st.cache_data(ttl=3600)
def load_all_matches():
    return loader.fetch_all_matches()

matches_df = load_all_matches()

# ---------------------------------------------------------
# Sidebar Navigation & Dynamic Match Selection
# ---------------------------------------------------------
st.sidebar.markdown('<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;"><span style="font-size: 1.8rem;">⚽</span><h2 style="margin: 0; color: #F8FAFC; font-size: 1.4rem; font-weight: 800;">Euro 2024</h2></div>', unsafe_allow_html=True)

search_query = st.sidebar.text_input("🔍 Search Team / Stage", placeholder="e.g. Spain, Germany, Final...")

stages = ["All"] + sorted(matches_df["stage"].dropna().unique().tolist()) if not matches_df.empty else ["All"]
selected_stage = st.sidebar.selectbox("Filter Tournament Stage", options=stages)

filtered_matches = loader.search_matches(query=search_query, stage_filter=selected_stage)
if filtered_matches.empty:
    filtered_matches = matches_df

match_options = filtered_matches["match_id"].tolist()
match_labels = filtered_matches.set_index("match_id")["display_label"].to_dict()

selected_match_id = st.sidebar.selectbox(
    "Select Fixture to Analyze",
    options=match_options,
    format_func=lambda x: match_labels.get(x, f"Match {x}")
)

st.sidebar.markdown("---")
api_key_input = st.sidebar.text_input("🔑 Google Gemini API Key (Optional)", type="password", help="Enter optional API key for real-time live LLM match report synthesis.")
ai_analyst = AITacticalAnalyst(api_key=api_key_input if api_key_input else None)

st.sidebar.markdown('<div style="margin-top: 20px; padding: 14px; background: rgba(30, 41, 59, 0.5); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.06); font-size: 0.78rem; color: #94A3B8;"><strong style="color: #38BDF8;">TacticalIQ Scout Tip:</strong> Select fixtures to switch telemetry datasets instantly. Gemini AI automatically falls back to domain-trained synthesis if API key is omitted.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Selected Match Events & Aggregates
# ---------------------------------------------------------
@st.cache_data(ttl=1800)
def load_events_for_match(m_id: int):
    events = loader.fetch_match_events(m_id)
    stats = loader.get_player_stats_for_events(events)
    return events, stats

events_df, player_stats_df = load_events_for_match(selected_match_id)
match_row = matches_df[matches_df["match_id"] == selected_match_id].iloc[0].to_dict() if not matches_df.empty else {}

# Fit ML Model for Player Tactical Role Clustering
ml_model = PlayerClusteringModel()
clustered_df = ml_model.train_and_predict(player_stats_df) if not player_stats_df.empty else pd.DataFrame()

# ---------------------------------------------------------
# Executive Top Header Banner
# ---------------------------------------------------------
render_top_header(match_row, events_df)

# ---------------------------------------------------------
# Main Tabs Layout (Clean Executive Display)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Match Overview & AI Report",
    "🎯 xG & Spatial Pitch Analytics",
    "🤖 ML Player Clustering & Radars",
    "🔍 AI Scout & Live Web Search",
    "🏆 Tournament Leaderboards",
    "⚔️ Cross-Fixture Head-to-Head"
])

with tab1:
    xg_summary = analytics_engine.compute_match_xg_summary(events_df)
    render_overview_tab(match_row, xg_summary, events_df, analytics_engine, visualizer, ai_analyst, live_search, loader, matches_df)

with tab2:
    render_spatial_analytics_tab(events_df, match_row, visualizer, analytics_engine)

with tab3:
    render_ml_clustering_tab(clustered_df, ml_model, visualizer)

with tab4:
    render_ai_scout_tab(match_row, ai_analyst, live_search)

with tab5:
    render_tournament_leaderboards_tab(loader)

with tab6:
    render_head_to_head_tab(matches_df, loader, analytics_engine, visualizer)

# ---------------------------------------------------------
# Executive Bottom Footer
# ---------------------------------------------------------
render_bottom_footer()

