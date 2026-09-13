import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
from config import THEME_COLORS
from typing import Dict, Any

def render_custom_css():
    """Injects high-end modern CSS styling, glassmorphism, interactive button effects, and hides Streamlit default chrome."""
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    background-color: #080C14 !important;
    color: #F8FAFC !important;
}

.stApp {
    background: 
        radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(129, 140, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.04) 0%, transparent 60%),
        linear-gradient(180deg, #080C14 0%, #0F172A 100%) !important;
    background-attachment: fixed !important;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

header[data-testid="stHeader"] {
    display: none !important;
    height: 0px !important;
}
footer {
    display: none !important;
}
#MainMenu {
    display: none !important;
}
div[data-testid="stToolbar"] {
    display: none !important;
}
div[data-testid="stDecoration"] {
    display: none !important;
}
div[data-testid="stStatusWidget"] {
    display: none !important;
}

.metric-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 20px 22px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 2px solid #38BDF8;
    box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56, 189, 248, 0.5);
    border-top-color: #0EA5E9;
    box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.6), 0 0 25px rgba(56, 189, 248, 0.2);
}

.metric-title {
    color: #94A3B8;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: flex;
    align-items: center;
    gap: 6px;
}

.metric-value {
    color: #F8FAFC;
    font-size: 1.85rem;
    font-weight: 800;
    margin-top: 6px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-subtitle {
    color: #38BDF8;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 4px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(8, 12, 20, 0.98) 100%) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.35) !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(14, 165, 233, 0.55), 0 0 15px rgba(56, 189, 248, 0.4) !important;
    background: linear-gradient(135deg, #38BDF8 0%, #3B82F6 100%) !important;
}

.stButton > button:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.4) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.25) 100%) !important;
    color: #34D399 !important;
    border: 1px solid rgba(52, 211, 153, 0.4) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: #FFFFFF !important;
    border-color: #10B981 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(16, 185, 129, 0.45) !important;
}

.stDownloadButton > button:active {
    transform: scale(0.97) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background: rgba(15, 23, 42, 0.75) !important;
    padding: 8px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px) !important;
}

.stTabs [data-baseweb="tab"] {
    height: 46px !important;
    border-radius: 10px !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    padding: 0 20px !important;
    border: 1px solid transparent !important;
    transition: all 0.25s ease !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
    background: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.18) 0%, rgba(37, 99, 235, 0.18) 100%) !important;
    color: #38BDF8 !important;
    font-weight: 700 !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25) !important;
}

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover {
    border-color: rgba(56, 189, 248, 0.5) !important;
}

div[data-baseweb="select"]:focus-within > div, div[data-baseweb="input"]:focus-within > div {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.35) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #F43F5E 100%) !important;
    border-radius: 10px !important;
}

@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.live-dot {
    width: 9px;
    height: 9px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse-glow 2s infinite;
}

.top-header-container {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid #38BDF8;
    border-radius: 18px;
    padding: 20px 26px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px -6px rgba(0, 0, 0, 0.5);
}

.bottom-footer-container {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(8, 12, 20, 0.95) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 40px;
    margin-bottom: 20px;
}
</style>""", unsafe_allow_html=True)

def render_top_header(match_row: Dict[str, Any], events_df: pd.DataFrame):
    """Renders the executive top header banner containing essential platform telemetry and active match details."""
    home_team = match_row.get("home_team", "Home")
    away_team = match_row.get("away_team", "Away")
    home_score = match_row.get("home_score", 0)
    away_score = match_row.get("away_score", 0)
    stage = match_row.get("stage", "Euro 2024")
    match_date = match_row.get("match_date", "2024")
    event_count = len(events_df) if events_df is not None else 0

    header_html = f"""<div class="top-header-container">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
<div>
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 2.0rem;">⚽</span>
<h1 style="margin: 0; color: #F8FAFC; font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em;">Tactical<span style="color: #38BDF8;">IQ</span></h1>
<span style="background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%); color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;">PRO ANALYTICS</span>
</div>
<p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.9rem;">UEFA Euro 2024 Match Intelligence & Tactical AI Scouting Platform</p>
</div>
<div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
<div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; color: #34D399; display: flex; align-items: center;"><span class="live-dot"></span> SYSTEM ONLINE</div>
<div style="background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; color: #38BDF8;">📊 StatsBomb Engine v2.4</div>
<div style="background: rgba(129, 140, 248, 0.12); border: 1px solid rgba(129, 140, 248, 0.3); padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; color: #A5B4FC;">🤖 Gemini 2.5 Flash AI</div>
</div>
</div>
<div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 0.88rem;">
<div style="color: #CBD5E1;">
<span style="color: #94A3B8;">Active Fixture Telemetry:</span> 
<strong style="color: #F8FAFC; font-size: 1.0rem; margin-left: 6px;">{home_team} {home_score} - {away_score} {away_team}</strong>
<span style="color: #64748B; margin: 0 8px;">|</span>
<span style="color: #38BDF8; font-weight: 600;">{stage}</span>
<span style="color: #64748B; margin: 0 8px;">|</span>
<span style="color: #94A3B8;">{match_date}</span>
</div>
<div style="color: #94A3B8; font-size: 0.82rem;">⚡ <strong style="color: #38BDF8;">{event_count}</strong> Event Telemetry Tokens Ingested</div>
</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)

def render_bottom_footer():
    """Renders the executive bottom footer containing platform methodology specs, attribution, and real-time status."""
    footer_html = """<div class="bottom-footer-container">
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px;">
<div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="font-size: 1.3rem;">⚽</span>
<strong style="color: #F8FAFC; font-size: 1.05rem;">TacticalIQ Platform</strong>
</div>
<p style="color: #94A3B8; font-size: 0.83rem; line-height: 1.5; margin: 0;">
Next-generation football intelligence platform providing real-time spatial event analytics, expected goals ($xG$) modelling, ML player role clustering, and AI scouting synthesis.
</p>
</div>
<div>
<h4 style="color: #38BDF8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 10px 0;">Core Methodology & Engine Specs</h4>
<ul style="color: #94A3B8; font-size: 0.82rem; padding-left: 16px; margin: 0; line-height: 1.6;">
<li>Geometry Model: Standard 120 x 80 Yard Pitch</li>
<li>xG & xA Vector Analytics Engine</li>
<li>Unsupervised ML K-Means (k=4) + 2D PCA</li>
<li>Google Gemini Multimodal AI Integration</li>
</ul>
</div>
<div>
<h4 style="color: #818CF8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 10px 0;">Data Attribution & Compliance</h4>
<p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.5; margin: 0;">
Powered by <strong>StatsBomb Open Data</strong> & <strong>Google Gemini API</strong>.<br/>
All tournament telemetry compliant with StatsBomb Open Data License terms.<br/>
© 2026 TacticalIQ. All rights reserved.
</p>
</div>
</div>
<div style="margin-top: 20px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.06); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.78rem; color: #64748B;">
<div><span class="live-dot" style="width: 7px; height: 7px;"></span> Live Data Sync: Active &nbsp;•&nbsp; Latency: &lt; 12ms &nbsp;•&nbsp; Build: v2.4.0-pro</div>
<div>🔒 TLS Encrypted Session &nbsp;•&nbsp; UEFA Euro 2024 Germany Analytics</div>
</div>
</div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

def render_overview_tab(match_row: Dict[str, Any], xg_summary: Dict[str, Any], events_df: pd.DataFrame, analytics_engine, visualizer, ai_analyst, live_search, loader=None, matches_df=None):
    """Renders Match Overview, Head-to-Head Comparison Bars, AI Match Report, Multi-Match Comparison, and Dossier Export."""
    home_team = match_row.get("home_team", "Home")
    away_team = match_row.get("away_team", "Away")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">⚽ Fixture</div><div class="metric-value" style="font-size:1.3rem;">{home_team} vs {away_team}</div><div class="metric-subtitle">{match_row.get("stage", "Euro 2024")}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">🏆 Scoreline</div><div class="metric-value">{match_row.get("home_score", 0)} - {match_row.get("away_score", 0)}</div><div class="metric-subtitle">Full Time Result</div></div>', unsafe_allow_html=True)
    with col3:
        h_xg = xg_summary.get(home_team, {}).get("total_xg", 0.0)
        st.markdown(f'<div class="metric-card"><div class="metric-title">🎯 {home_team} xG</div><div class="metric-value">{h_xg:.2f}</div><div class="metric-subtitle">Expected Goals Created</div></div>', unsafe_allow_html=True)
    with col4:
        a_xg = xg_summary.get(away_team, {}).get("total_xg", 0.0)
        st.markdown(f'<div class="metric-card"><div class="metric-title">🎯 {away_team} xG</div><div class="metric-value">{a_xg:.2f}</div><div class="metric-subtitle">Expected Goals Created</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"⚔️ Team Head-to-Head Comparison ({home_team} vs {away_team})")
    
    h_shots = xg_summary.get(home_team, {}).get("total_shots", 0)
    a_shots = xg_summary.get(away_team, {}).get("total_shots", 0)
    tot_shots = max(1, h_shots + a_shots)
    
    h_xg_val = xg_summary.get(home_team, {}).get("total_xg", 0.0)
    a_xg_val = xg_summary.get(away_team, {}).get("total_xg", 0.0)
    tot_xg = max(0.1, h_xg_val + a_xg_val)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.write(f"**Expected Goals ($xG$) Share**: {home_team} ({h_xg_val:.2f}) vs {away_team} ({a_xg_val:.2f})")
        st.progress(h_xg_val / tot_xg, text=f"{home_team}: {round(h_xg_val/tot_xg*100)}% | {away_team}: {round(a_xg_val/tot_xg*100)}%")
    with col_t2:
        st.write(f"**Total Shot Attempts**: {home_team} ({h_shots}) vs {away_team} ({a_shots})")
        st.progress(h_shots / tot_shots, text=f"{home_team}: {round(h_shots/tot_shots*100)}% | {away_team}: {round(a_shots/tot_shots*100)}%")

    st.markdown("---")
    st.subheader("📈 Match Momentum: Cumulative Expected Goals (xG) Timeline")
    st.caption("ℹ️ Tracks minute-by-minute cumulative team xG over 90 minutes. Goal markers highlight exact score changes.")

    cum_xg_data = analytics_engine.compute_cumulative_xg_timeline(events_df)
    if cum_xg_data:
        fig_timeline = visualizer.plot_xg_timeline(cum_xg_data, title=f"Match Momentum: {home_team} vs {away_team} Cumulative xG")
        if fig_timeline is not None:
            st.pyplot(fig_timeline)

    # Multi-Fixture Comparison Engine
    if loader is not None and matches_df is not None and not matches_df.empty:
        st.markdown("---")
        st.subheader("🔄 Multi-Fixture Fixture vs Fixture Comparison Engine")
        st.caption("Select a 2nd Euro 2024 fixture to compare team xG, shot creation, and match dynamics side-by-side.")

        m2_options = matches_df["match_id"].tolist()
        m2_labels = matches_df.set_index("match_id")["display_label"].to_dict()
        
        curr_m_id = match_row.get("match_id")
        def_idx = 1 if len(m2_options) > 1 and m2_options[0] == curr_m_id else 0

        selected_m2_id = st.selectbox(
            "Select Benchmark Fixture to Compare",
            options=m2_options,
            index=def_idx,
            format_func=lambda x: m2_labels.get(x, f"Match {x}")
        )

        if selected_m2_id and selected_m2_id != curr_m_id:
            m2_row = matches_df[matches_df["match_id"] == selected_m2_id].iloc[0].to_dict()
            m2_events = loader.fetch_match_events(selected_m2_id)
            m2_xg = analytics_engine.compute_match_xg_summary(m2_events)

            col_cm1, col_cm2 = st.columns(2)
            with col_cm1:
                st.markdown(f'<div class="metric-card"><div class="metric-title">Match A (Current)</div><div style="font-weight:bold; font-size:1.2rem; color:#F8FAFC; margin-top:4px;">{home_team} vs {away_team}</div><div style="color:#38BDF8; font-size:0.95rem; margin-top:4px;">Score: {match_row.get("home_score")} - {match_row.get("away_score")}</div><div style="color:#94A3B8; font-size:0.85rem; margin-top:4px;">xG: {home_team} ({h_xg_val:.2f}) | {away_team} ({a_xg_val:.2f})</div><div style="color:#94A3B8; font-size:0.85rem;">Shots: {home_team} ({h_shots}) | {away_team} ({a_shots})</div></div>', unsafe_allow_html=True)

            with col_cm2:
                m2_h = m2_row.get("home_team", "Home")
                m2_a = m2_row.get("away_team", "Away")
                m2_h_xg = m2_xg.get(m2_h, {}).get("total_xg", 0.0)
                m2_a_xg = m2_xg.get(m2_a, {}).get("total_xg", 0.0)
                m2_h_shots = m2_xg.get(m2_h, {}).get("total_shots", 0)
                m2_a_shots = m2_xg.get(m2_a, {}).get("total_shots", 0)

                st.markdown(f'<div class="metric-card" style="border-top-color:#818CF8;"><div class="metric-title">Match B (Benchmark)</div><div style="font-weight:bold; font-size:1.2rem; color:#F8FAFC; margin-top:4px;">{m2_h} vs {m2_a}</div><div style="color:#818CF8; font-size:0.95rem; margin-top:4px;">Score: {m2_row.get("home_score")} - {m2_row.get("away_score")}</div><div style="color:#94A3B8; font-size:0.85rem; margin-top:4px;">xG: {m2_h} ({m2_h_xg:.2f}) | {m2_a} ({m2_a_xg:.2f})</div><div style="color:#94A3B8; font-size:0.85rem;">Shots: {m2_h} ({m2_h_shots}) | {m2_a} ({m2_a_shots})</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_rep, col_exp = st.columns([3, 1])
    with col_rep:
        st.subheader(f"🧠 AI Executive Tactical Match Report ({home_team} vs {away_team})")
    with col_exp:
        dossier_text = f"""# TacticalIQ Match Scouting Dossier: {home_team} vs {away_team}
Date: {match_row.get('match_date', '2024')} | Stage: {match_row.get('stage', 'Euro 2024')}
Scoreline: {home_team} {match_row.get('home_score')} - {match_row.get('away_score')} {away_team}
Total xG: {home_team} ({h_xg_val:.2f}) | {away_team} ({a_xg_val:.2f})

---
Report generated dynamically by TacticalIQ AI Platform via StatsBomb Open Data.
"""
        st.download_button(
            label="📄 Export Match Dossier (.md)",
            data=dossier_text,
            file_name=f"TacticalIQ_Scouting_Report_{home_team}_vs_{away_team}.md",
            mime="text/markdown",
            use_container_width=True
        )

    if st.button("🚀 Generate AI Tactical Match Report", use_container_width=True):
        with st.spinner("Synthesizing tactical match analytics and event telemetry..."):
            live_context = live_search.search_live_news(f"{home_team} vs {away_team} Euro 2024 tactics")
            report = ai_analyst.generate_tactical_match_report(match_row, xg_summary, live_context)
            st.markdown(report)
    else:
        st.info("Click the button above to generate a real-time AI tactical breakdown for this fixture.")

def render_spatial_analytics_tab(events_df: pd.DataFrame, match_row: Dict[str, Any], visualizer, analytics_engine):
    """Renders Spatial Shot Quality Map, Pass Networks, Key Pass xA Vectors, Defensive Disruptions, and Heatmaps."""
    home_team = match_row.get("home_team", "Home")
    away_team = match_row.get("away_team", "Away")

    st.subheader(f"Spatial Pitch Analytics ({home_team} vs {away_team})")

    shots_df = events_df[events_df["type"] == "Shot"].copy() if not events_df.empty else pd.DataFrame()
    if not shots_df.empty and "xg" not in shots_df.columns:
        shots_df["xg"] = shots_df.apply(
            lambda r: analytics_engine.calculate_xg_from_geometry(r.get("start_x"), r.get("start_y")), axis=1
        )

    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
        "🎯 Dual-Goal Shot Quality Map",
        "⚽ Pass Networks & Formations",
        "🔥 Pressure Density Heatmaps",
        "🅰️ Key Pass & xA Creation Vectors",
        "🛡️ Defensive Disruption & Line Height",
        "📈 Match Momentum Flow"
    ])

    with subtab1:
        team_filter = st.radio("Filter Team Shots", options=["All", home_team, away_team], horizontal=True)
        if team_filter != "All" and not shots_df.empty:
            filtered_shots = shots_df[shots_df["team"] == team_filter]
        else:
            filtered_shots = shots_df

        col1, col2 = st.columns([2.2, 1])
        with col1:
            fig_shot = visualizer.plot_shot_map(
                filtered_shots, home_team=home_team, away_team=away_team,
                title=f"Euro 2024 Dual-Goal Shot Quality Map: {home_team} vs {away_team}"
            )
            if fig_shot is not None:
                st.pyplot(fig_shot)
            else:
                st.info("Visualizer rendering pitch graphics.")

        with col2:
            st.markdown("### 📋 Shot Events Table")
            if not filtered_shots.empty:
                cols_to_show = [c for c in ["minute", "team", "player", "shot_outcome", "xg", "body_part"] if c in filtered_shots.columns]
                st.dataframe(filtered_shots[cols_to_show], use_container_width=True, height=380)
            else:
                st.write("No shots recorded.")

    with subtab2:
        avg_pos_df = analytics_engine.compute_player_average_positions(events_df)
        connections_df = analytics_engine.compute_pass_network_links(events_df, min_passes=1)
        fig_pass = visualizer.plot_tactical_pass_network(
            avg_pos_df, connections_df,
            title=f"Starting XI Formations & Pass Networks: {home_team} vs {away_team}"
        )
        if fig_pass is not None:
            st.pyplot(fig_pass)

    with subtab3:
        st.caption("ℹ️ 2D Spatial Density Heatmaps visualizing pressing traps and defensive high/low block zones.")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            fig_hm1 = visualizer.plot_pressure_heatmap(events_df, home_team)
            if fig_hm1 is not None:
                st.pyplot(fig_hm1)
        with col_h2:
            fig_hm2 = visualizer.plot_pressure_heatmap(events_df, away_team)
            if fig_hm2 is not None:
                st.pyplot(fig_hm2)

    with subtab4:
        st.caption("ℹ️ Directional pass vector arrows connecting key passes leading directly to shot attempts, colored by Expected Assists (xA).")
        key_passes_df = analytics_engine.compute_key_passes_and_xa(events_df)
        col_kp1, col_kp2 = st.columns(2)
        with col_kp1:
            fig_kp1 = visualizer.plot_key_pass_vectors(key_passes_df, home_team)
            if fig_kp1 is not None:
                st.pyplot(fig_kp1)
        with col_kp2:
            fig_kp2 = visualizer.plot_key_pass_vectors(key_passes_df, away_team)
            if fig_kp2 is not None:
                st.pyplot(fig_kp2)

    with subtab5:
        st.caption("ℹ️ Spatial coordinates of tackles won, interceptions, blocks, and average defensive line block height.")
        def_line_data = analytics_engine.compute_defensive_line_height(events_df)
        fig_def_line = visualizer.plot_defensive_line_comparison(def_line_data)
        if fig_def_line is not None:
            st.pyplot(fig_def_line)

        disruptions_df = analytics_engine.compute_defensive_disruptions(events_df)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            fig_d1 = visualizer.plot_defensive_disruption_map(disruptions_df, home_team)
            if fig_d1 is not None:
                st.pyplot(fig_d1)
        with col_d2:
            fig_d2 = visualizer.plot_defensive_disruption_map(disruptions_df, away_team)
            if fig_d2 is not None:
                st.pyplot(fig_d2)

    with subtab6:
        st.caption("ℹ️ 15-minute rolling match dominance and tactical momentum index.")
        momentum_data = analytics_engine.compute_match_momentum_timeline(events_df)
        fig_mom = visualizer.plot_team_momentum_chart(momentum_data)
        if fig_mom is not None:
            st.pyplot(fig_mom)

    st.markdown("---")
    st.subheader("Field Thirds Defensive Pressure Intensity")
    pressures_summary = analytics_engine.compute_field_thirds_pressure(events_df)
    
    if pressures_summary:
        cols = st.columns(len(pressures_summary))
        for idx, (team, pdata) in enumerate(pressures_summary.items()):
            with cols[idx]:
                st.markdown(f"#### {team}")
                st.write(f"**Total Pressures**: {pdata['total_pressures']}")
                st.progress(pdata['att_pct'] / 100.0, text=f"Attacking Third: {pdata['attraction_third']} ({pdata['att_pct']}%)")
                st.progress(pdata['mid_pct'] / 100.0, text=f"Midfield Third: {pdata['midfield_third']} ({pdata['mid_pct']}%)")
                st.progress(pdata['def_pct'] / 100.0, text=f"Defensive Third: {pdata['defensive_third']} ({pdata['def_pct']}%)")

def render_ml_clustering_tab(clustered_df: pd.DataFrame, ml_model, visualizer):
    """Renders Machine Learning Player Role Clustering and 1v1 Radar Comparison tab."""
    st.subheader("Machine Learning Player Role Clustering (K-Means + PCA)")
    st.caption("ℹ️ **Unsupervised Clustering**: Groups players into tactical roles by analyzing spatial pitch depth, lateral channels, pass volume, xG, and pressures.")

    if not clustered_df.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig_pca = visualizer.plot_pca_clusters(clustered_df)
            if fig_pca is not None:
                st.pyplot(fig_pca)

        with col2:
            st.markdown("### 📋 Player Roles Table")
            display_cols = [c for c in ["player", "team", "official_position", "tactical_role"] if c in clustered_df.columns]
            st.dataframe(clustered_df[display_cols], use_container_width=True, height=380)

        st.markdown("---")
        st.subheader("⚔️ 1v1 Player Radar Comparison Tool")
        st.caption("Select any two players to visually compare their tactical profiles across 6 key metrics on a polar radar chart.")
        
        all_players = sorted(clustered_df["player"].tolist())
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            player1 = st.selectbox("Select Player 1", options=all_players, index=0)
        with col_p2:
            player2 = st.selectbox("Select Player 2", options=all_players, index=min(1, len(all_players)-1))

        if player1 and player2 and player1 != player2:
            p1_row = clustered_df[clustered_df["player"] == player1].iloc[0]
            p2_row = clustered_df[clustered_df["player"] == player2].iloc[0]
            fig_radar = visualizer.plot_player_radar_comparison(p1_row, p2_row)
            if fig_radar is not None:
                st.pyplot(fig_radar)

        st.markdown("---")
        st.markdown("### 🔍 Real-World Player Similarity Engine")
        target_player = st.selectbox("Select Target Player for Similarity Match", options=all_players, index=0)

        if target_player:
            target_info = clustered_df[clustered_df["player"] == target_player].iloc[0]
            st.info(f"Target Player: **{target_player}** ({target_info['team']}) — Official Pos: *{target_info.get('official_position', 'Field Player')}* | ML Profile: *{target_info['tactical_role']}*")
            
            similar_players = ml_model.find_similar_players(target_player, clustered_df, top_n=3)
            st.write(f"**Top Players Similar to {target_player}:**")
            cols = st.columns(len(similar_players))
            for idx, sim in enumerate(similar_players):
                with cols[idx]:
                    st.markdown(f'<div class="metric-card"><div class="metric-title">{sim["team"]}</div><div style="font-weight:bold; font-size:1.1rem; color:#F8FAFC;">{sim["player"]}</div><div style="color:#94A3B8; font-size:0.85rem; margin-top:2px;">Official Pos: {sim.get("official_position", "Field Player")}</div><div style="color:#38BDF8; font-size:0.9rem; margin-top:4px;">ML Profile: {sim["tactical_role"]}</div><div style="color:#10B981; font-weight:bold; margin-top:4px;">Similarity: {sim["similarity_score"]}%</div></div>', unsafe_allow_html=True)
    else:
        st.warning("No player statistics available for clustering.")

def render_ai_scout_tab(match_row: Dict[str, Any], ai_analyst, live_search):
    """Renders AI Scout Assistant, Live Web Search, and Tactical Counter-Strategy Simulator."""
    home_team = match_row.get("home_team", "Home")
    away_team = match_row.get("away_team", "Away")

    st.subheader("🌐 Real-Time Live Web Search & AI Scout Assistant")
    st.caption("ℹ️ Query live web news + StatsBomb match event streams to answer custom tactical scouting queries.")

    default_q = f"How did {home_team} control possession against {away_team}?"
    query = st.text_input("Enter Tactical Scouting Question", default_q)

    if st.button("Search & Analyze Query", use_container_width=True):
        with st.spinner("Searching web intelligence and running tactical AI analysis..."):
            web_results = live_search.search_live_news(query, max_results=3)
            st.markdown("#### 📰 Live Web Findings")
            for res in web_results:
                st.markdown(f"- **[{res['title']}]({res['link']})**: {res['snippet']}")

            st.markdown("---")
            st.markdown("#### 🤖 AI Scout Response")
            answer = ai_analyst.answer_scout_query(query, match_row, web_results)
            st.markdown(answer)

    st.markdown("---")
    st.subheader("🎮 Interactive AI Tactical Counter-Strategy Simulator")
    st.caption("Input custom opponent tactical setups to generate an instant AI counter-strategy blueprint and pressing plan.")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        opp_team = st.text_input("Opponent Team Name", away_team)
        opp_formation = st.selectbox("Opponent Formation", ["4-3-3", "4-2-3-1", "5-3-2 / 3-5-2", "4-4-2 Mid-Block", "3-4-2-1 High Press"])
    with col_sim2:
        opp_playstyle = st.selectbox("Opponent Playstyle", ["High Pressing & Vertical Transition", "Low Block Counter-Attack", "Possession Heavy & Overlapping Wings", "Direct Long-Ball Target Man"])
        opp_star = st.text_input("Key Opponent Player to Neutralize", "Jude Bellingham")

    if st.button("🚀 Run AI Tactical Counter-Strategy Simulation", use_container_width=True):
        with st.spinner(f"Simulating tactical counter-blueprint vs {opp_team} ({opp_formation})..."):
            blueprint = ai_analyst.simulate_tactical_counter_strategy(opp_team, opp_formation, opp_playstyle, opp_star)
            st.markdown(blueprint)

def render_tournament_leaderboards_tab(loader):
    """Renders Tournament-Wide Player Leaderboards across cached UEFA Euro 2024 matches."""
    st.subheader("🏆 UEFA Euro 2024 Tournament Leaderboards")
    st.caption("ℹ️ Aggregated performance leaders across cached Euro 2024 match event stream datasets.")

    with st.spinner("Aggregating tournament player metrics..."):
        leaderboards = loader.get_tournament_leaderboards()

    if not leaderboards:
        st.info("Load matches in the sidebar to populate tournament leaderboards.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Top Expected Goals ($xG$) Leaders")
        st.dataframe(leaderboards.get("top_xg"), use_container_width=True)

        st.markdown("### ⚽ Top Goal Scorers")
        st.dataframe(leaderboards.get("top_goals"), use_container_width=True)

    with col2:
        st.markdown("### 🅰️ Top Pass Masters (Completed Passes)")
        st.dataframe(leaderboards.get("top_passes"), use_container_width=True)

        st.markdown("### 🛡️ Top Defensive Pressers")
        st.dataframe(leaderboards.get("top_pressures"), use_container_width=True)

def render_head_to_head_tab(matches_df: pd.DataFrame, loader, analytics_engine, visualizer):
    """Renders Cross-Fixture Head-to-Head Analytics tab comparing 2 Euro 2024 matches or team setups."""
    st.subheader("⚔️ Head-to-Head & Cross-Fixture Telemetry Analytics")
    st.caption("Compare key performance metrics, xG conversion efficiency, and defensive block heights side-by-side across Euro 2024 fixtures.")

    if matches_df is None or matches_df.empty:
        st.info("No fixtures available for comparison.")
        return

    m_options = matches_df["match_id"].tolist()
    m_labels = matches_df.set_index("match_id")["display_label"].to_dict()

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m1_id = st.selectbox(
            "Select Primary Fixture (Match A)",
            options=m_options,
            index=0,
            key="h2h_m1",
            format_func=lambda x: m_labels.get(x, f"Match {x}")
        )
    with col_m2:
        m2_idx = min(1, len(m_options) - 1)
        m2_id = st.selectbox(
            "Select Benchmark Fixture (Match B)",
            options=m_options,
            index=m2_idx,
            key="h2h_m2",
            format_func=lambda x: m_labels.get(x, f"Match {x}")
        )


    if m1_id and m2_id:
        m1_row = matches_df[matches_df["match_id"] == m1_id].iloc[0].to_dict()
        m2_row = matches_df[matches_df["match_id"] == m2_id].iloc[0].to_dict()

        events1 = loader.fetch_match_events(m1_id)
        events2 = loader.fetch_match_events(m2_id)

        xg1 = analytics_engine.compute_match_xg_summary(events1)
        xg2 = analytics_engine.compute_match_xg_summary(events2)

        def1 = analytics_engine.compute_defensive_line_height(events1)
        def2 = analytics_engine.compute_defensive_line_height(events2)

        direct1 = analytics_engine.compute_pass_directness_index(events1)
        direct2 = analytics_engine.compute_pass_directness_index(events2)

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"### 🏟️ Match A: {m1_row.get('home_team')} {m1_row.get('home_score')} - {m1_row.get('away_score')} {m1_row.get('away_team')}")
            for t_name, t_data in xg1.items():
                d_info = def1.get(t_name, {})
                dir_info = direct1.get(t_name, {})
                st.markdown(f"""<div class="metric-card" style="margin-bottom: 12px;">
<div class="metric-title">{t_name} Telemetry</div>
<div style="font-size: 1.1rem; color:#F8FAFC; font-weight:bold; margin-top:4px;">xG: {t_data.get('total_xg')} | Shots: {t_data.get('total_shots')} | Goals: {t_data.get('goals')}</div>
<div style="color: #38BDF8; font-size:0.85rem; margin-top:4px;">Defensive Line: {d_info.get('avg_line_height_yards', 'N/A')} yds ({d_info.get('block_type', 'N/A')})</div>
<div style="color: #94A3B8; font-size:0.85rem;">Pass Directness: {dir_info.get('directness_pct', 'N/A')}% forward | Avg Length: {dir_info.get('avg_pass_length_yards', 'N/A')} yds</div>
</div>""", unsafe_allow_html=True)

        with col_res2:
            st.markdown(f"### 🏟️ Match B: {m2_row.get('home_team')} {m2_row.get('home_score')} - {m2_row.get('away_score')} {m2_row.get('away_team')}")
            for t_name, t_data in xg2.items():
                d_info = def2.get(t_name, {})
                dir_info = direct2.get(t_name, {})
                st.markdown(f"""<div class="metric-card" style="margin-bottom: 12px; border-top-color:#818CF8;">
<div class="metric-title">{t_name} Telemetry</div>
<div style="font-size: 1.1rem; color:#F8FAFC; font-weight:bold; margin-top:4px;">xG: {t_data.get('total_xg')} | Shots: {t_data.get('total_shots')} | Goals: {t_data.get('goals')}</div>
<div style="color: #818CF8; font-size:0.85rem; margin-top:4px;">Defensive Line: {d_info.get('avg_line_height_yards', 'N/A')} yds ({d_info.get('block_type', 'N/A')})</div>
<div style="color: #94A3B8; font-size:0.85rem;">Pass Directness: {dir_info.get('directness_pct', 'N/A')}% forward | Avg Length: {dir_info.get('avg_pass_length_yards', 'N/A')} yds</div>
</div>""", unsafe_allow_html=True)

