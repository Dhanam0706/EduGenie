"""Shared Gemini service used by every EduGenie module.

The feature modules (qna.py, quiz_module.py, ...) only build prompts. The call to Gemini,
API-key handling, model fallback and user-safe error messages live here, in one place.

Depends on: config.py, google-genai
"""
import logging
import time

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

import config

logger = logging.getLogger("edugenie")

# HTTP codes that mean "this model is retired, busy or down": try the next model in the chain.
RETRY_NEXT_MODEL = {404, 429, 500, 502, 503, 504}


class GeminiError(Exception):
    """An error whose message is safe to show to the user."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def gemini_configured() -> bool:
    return bool(config.get_api_key())


def _model_chain() -> list:
    """Configured model first, then the fallbacks, without duplicates."""
    chain = []
    for name in [config.get_model(), *config.GEMINI_FALLBACK_MODELS]:
        if name not in chain:
            chain.append(name)
    return chain


def _is_key_problem(code, message: str) -> bool:
    return code in (401, 403) or (code == 400 and "api key" in message.lower())


def generate(prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    api_key = config.get_api_key()
    if not api_key:
        raise GeminiError(
            "The Gemini API key is missing. Add GEMINI_API_KEY to your .env file "
            "and restart the server.",
            status_code=500,
        )

    started = time.monotonic()
    last_code = None
    for model in _model_chain():
        if time.monotonic() - started > config.GEMINI_TOTAL_BUDGET_SECONDS:
            break
        try:
            client = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=config.GEMINI_TIMEOUT_SECONDS * 1000),
            )
            response = client.models.generate_content(model=model, contents=prompt)
        except genai_errors.APIError as exc:
            code = getattr(exc, "code", None)
            last_code = code
            logger.warning("Gemini API error (model=%s, code=%s)", model, code)
            if _is_key_problem(code, str(getattr(exc, "message", "") or "")):
                raise GeminiError("The Gemini API key was rejected. Please check GEMINI_API_KEY.")
            if code in RETRY_NEXT_MODEL:
                continue
            raise GeminiError("Gemini could not complete the request. Please try again.")
        except Exception:
            # Network problems and anything unexpected. Details stay in the server log only.
            logger.exception("Could not reach Gemini")
            raise GeminiError("Could not reach Gemini. Check your internet connection and try again.")

        text = getattr(response, "text", None)
        if text and text.strip():
            return text.strip()
        raise GeminiError("Gemini returned an empty answer. Please try rephrasing your request.")

    if last_code == 429:
        raise GeminiError(
            "Gemini is receiving too many requests right now. Please wait a moment and try again.",
            status_code=429,
        )
    raise GeminiError("Gemini is not available right now. Please try again in a few minutes.")
