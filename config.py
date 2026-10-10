"""Central configuration for EduGenie.

All settings come from environment variables (loaded from `.env` when present),
so no secret ever lives in the source code.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # real environment variables always win over the .env file

BASE_DIR = Path(__file__).resolve().parent

# --- Gemini ------------------------------------------------------------------
DEFAULT_MODEL = "gemini-3.8-flash"
# Tried in order when the primary model is retired / unavailable (HTTP 404/429/5xx).
GEMINI_FALLBACK_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]
GEMINI_TIMEOUT_SECONDS = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "25"))
GEMINI_TOTAL_BUDGET_SECONDS = int(os.getenv("GEMINI_TOTAL_BUDGET_SECONDS", "60"))

# --- Input limits ------------------------------------------------------------
MAX_INPUT_CHARS = 8000


def get_api_key() -> str:
    """Read the key at call time so tests (and a restarted server) always see the current value."""
    return (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()


def get_model() -> str:
    return (os.getenv("GEMINI_MODEL") or DEFAULT_MODEL).strip() or DEFAULT_MODEL
