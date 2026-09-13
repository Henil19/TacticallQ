import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Data Files
SAMPLE_MATCHES_FILE = DATA_DIR / "sample_euro2024_matches.json"
SAMPLE_EVENTS_FILE = DATA_DIR / "sample_final_events.json"

# Pitch Dimensions (StatsBomb standard: 120 yards long x 80 yards wide)
PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0
GOAL_X = 120.0
GOAL_Y = 40.0

# Gemini API Configuration
GEMINI_MODEL = "gemini-2.5-flash"
API_KEY_ENV_VAR = "GEMINI_API_KEY"

# ML Model Settings
N_CLUSTERS = 4
RANDOM_STATE = 42

# Styling Palette (Modern Dark / Tactical Dashboard Theme)
THEME_COLORS = {
    "background": "#080C14",
    "card_bg": "#0F172A",
    "primary": "#38BDF8",
    "secondary": "#818CF8",
    "accent": "#F43F5E",
    "text": "#F8FAFC",
    "pitch_bg": "#0F192C",
    "pitch_lines": "#334155"
}
