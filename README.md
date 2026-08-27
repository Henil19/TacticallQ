# ⚽ TacticalIQ: UEFA Euro 2024 AI Football Analytics Platform

**TacticalIQ** is a modular, medium-tier football data analysis and AI scouting platform designed for **UEFA Euro 2024**. The project integrates traditional statistical metrics (Expected Goals $xG$, Expected Assists $xA$, Pitch Pressure Density), Machine Learning (K-Means Player Tactical Role Clustering & PCA Spatial Reduction), and Generative AI (LLM Tactical Analyst via Gemini API) along with dual-source data handling (local StatsBomb event datasets + real live web search).

---

## 💡 Why Use AI in Football Data Analysis?

Traditional football analytics relies heavily on quantitative metrics ($xG$, $xA$, pass completion %, pressures per 90). While numbers measure **what** happened on the pitch, **AI unlocks *why* and *how* it happened**:

1. **Contextual & Narrative Synthesis**: $xG$ calculates shot probability based on distance and angle, but AI synthesizes spatial defensive compacting, transition tempo, and player body orientation into human-understandable tactical insights.
2. **Natural Language Querying (NLQ)**: Enables non-technical staff (coaches, performance directors, scouts) to ask complex tactical questions (*"How did Spain break down England's mid-block in the Euro 2024 final?"*) without writing SQL or Python queries.
3. **Multi-Source Data Fusion**: Combines rigid local match event streams with live unstructured web news, team press releases, squad injury updates, and player market dynamics.
4. **Automated Scouting Dossiers**: Converts high-dimensional ML clustering output into executive pre-match scouting summaries and player target recommendations.

---

## 🏗️ Project Architecture & Modular Design

```
Game-State/
├── config.py                      # Application configurations, pitch constants, styling palette
├── requirements.txt               # Project dependencies (pandas, scikit-learn, streamlit, etc.)
├── README.md                      # Complete documentation & usage guide
├── test_pipeline.py               # Automated pipeline verification script
├── data/
│   ├── sample_euro2024_matches.json  # Euro 2024 match metadata index
│   └── sample_final_events.json     # StatsBomb event stream data for Euro 2024 Final
├── modules/
│   ├── __init__.py
│   ├── data_loader.py             # Parses local JSON/CSV StatsBomb event stream datasets
│   ├── live_search.py             # Real-time web search & scraper for live news & stats
│   ├── analytics_engine.py        # Computes xG, xA, field pressure density & pass connections
│   ├── ml_clustering.py           # K-Means clustering & PCA player tactical role mapping
│   ├── ai_analyst.py              # Gemini LLM tactical match reporting & scout Q&A engine
│   └── visualization.py           # Standard 120x80 yard pitch rendering & PCA scatter plots
└── app.py                         # Streamlit interactive Web Application dashboard
```

---

## 🛠️ Languages & Tech Stack

- **Python 3.10+**: Core programming language.
  - **Data Manipulation**: `pandas`, `numpy`
  - **Machine Learning**: `scikit-learn` (K-Means, PCA, StandardScaler)
  - **Visualization**: `matplotlib`, `seaborn`
  - **AI SDK**: `google-genai` (Google Gemini 2.5 API)
  - **Live Web Search**: `duckduckgo-search`, `requests`, `beautifulsoup4`
  - **Interactive Web UI**: `streamlit`
- **JSON / SQL**: Data representation standards for StatsBomb event streams.
- **HTML / CSS**: Custom styling for glassmorphic Streamlit dashboard components.

---

## 🚀 Quickstart & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key (Optional)
Set your Google Gemini API key as an environment variable (or enter it in the Streamlit UI sidebar):
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/macOS
export GEMINI_API_KEY="your_api_key_here"
```
*(Note: If no API key is provided, the platform automatically utilizes built-in structured domain heuristic fallbacks).*

### 3. Run Pipeline Verification Tests
```bash
python test_pipeline.py
```

### 4. Launch Interactive Web Dashboard
```bash
streamlit run app.py
```

---

## 📊 Modules Overview

### 1. Data Loader (`modules/data_loader.py`)
Parses StatsBomb event data into structured DataFrames, extracting shot locations $(X,Y)$, pass recipients, pressure zones, and player performance aggregates.

### 2. Analytics Engine (`modules/analytics_engine.py`)
Implements trigonometric and spatial $xG$ formulas ($d = \sqrt{\Delta x^2 + \Delta y^2}$, goal angle $\theta$), Expected Assists ($xA$), and pressure intensity across field thirds.

### 3. ML Player Clustering (`modules/ml_clustering.py`)
Uses K-Means clustering ($K=4$) and PCA 2D projection to classify players into roles (*Creative Playmaker*, *Goal-Threat Attacker*, *High-Pressing Midfielder*, *Defensive Anchor*) and provides Euclidean similarity scoring.

### 4. Live Search Engine (`modules/live_search.py`)
Executes real-time live web queries via DuckDuckGo and web fallback scrapers to bring current news, tactical previews, and transfer market values into the analysis pipeline.

### 5. AI Tactical Analyst (`modules/ai_analyst.py`)
Combines numerical event outputs and live search results into executive match reports and interactive scout Q&A responses via Google Gemini LLM.

### 6. Pitch Visualizer (`modules/visualization.py`)
Renders pitch graphics including shot maps (sized by $xG$, colored by outcome) and PCA scatter plots.

---

## 📜 License
MIT License - Free for educational and analytical use. Data powered by StatsBomb Open Data.
