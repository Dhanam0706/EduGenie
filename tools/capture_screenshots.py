"""Drive the running app in a real browser (Playwright) and save screenshots as test/demo evidence.

Needs a real GEMINI_API_KEY in .env (the screenshots show real Gemini answers). Usage:
    uvicorn main:app          # in another terminal
    python tools/capture_screenshots.py [base_url] [output_dir]
Exits non-zero if a JavaScript error or a failed step is detected.
"""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "docs-src/assets")
OUT.mkdir(parents=True, exist_ok=True)

NOTES = (
    "Photosynthesis is the process by which green plants use sunlight, water and carbon dioxide "
    "to make glucose and oxygen. It happens in the chloroplasts. The light reactions capture "
    "energy in the thylakoids and the Calvin cycle builds sugar in the stroma. Photosynthesis "
    "supplies the oxygen we breathe and the food at the base of almost every food chain."
)


def main() -> int:
    errors = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.getenv("CHROMIUM_PATH") or None)
        page = browser.new_page(viewport={"width": 1100, "height": 900})
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        # The empty-input step is handled in JavaScript, so any console error is a real failure.
        page.on("console", lambda m: errors.append(f"console: {m.text}") if m.type == "error" else None)

        def shot(name):
            page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)

        def submit(task, text):
            page.select_option("#task", task)
            page.fill("#user-input", text)
            page.click("#submit-btn")
            page.wait_for_selector("#result:not([hidden])", timeout=90000)

        page.goto(BASE + "/")
        shot("01_home")

        submit("qa", "What is a Turing machine?")
        shot("02_ask_question")

        page.check("#followup")
        submit("qa", "Can you give an example?")
        shot("03_follow_up")

        submit("explain", "Operating system process synchronization")
        shot("04_explain")

        submit("summarize", NOTES)
        shot("05_summary")

        submit("quiz", "The Pythagoras theorem")
        page.click(".quiz-card:first-child .quiz-option >> nth=0")
        shot("06_quiz")

        submit("recommend", "SQL")
        shot("07_learning_path")

        # Empty input shows a friendly message and sends nothing to the server.
        page.fill("#user-input", "")
        page.click("#submit-btn")
        page.wait_for_selector("#status.error")
        shot("08_empty_input_error")

        browser.close()
    if errors:
        print("FAILED - browser errors:\n  " + "\n  ".join(errors))
        return 1
    print(f"OK - UI flow passed; screenshots in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
