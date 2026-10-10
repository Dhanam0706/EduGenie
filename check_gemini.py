"""Activity 1.3 - validate Gemini connectivity.

Usage:  python check_gemini.py
Needs GEMINI_API_KEY in .env. Tries the configured model, then the fallback chain,
and prints which model to set as GEMINI_MODEL.
"""
import sys

import config
from gemini_utils import _model_chain, gemini_configured


def main() -> int:
    if not gemini_configured():
        print("FAIL: GEMINI_API_KEY is not set. Copy .env.example to .env and add your key.")
        return 1
    from google import genai

    client = genai.Client(api_key=config.get_api_key())
    for model in _model_chain():
        try:
            text = client.models.generate_content(model=model, contents="Reply with the single word: ready").text
            print(f"[text ] {model}: {text.strip()[:60]}")
            print(f"\nOK: set GEMINI_MODEL={model} in .env")
            return 0
        except Exception as exc:
            print(f"[skip ] {model}: {str(exc)[:120]}")
    print("FAIL: no model responded. Check the API key, quota and network.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
