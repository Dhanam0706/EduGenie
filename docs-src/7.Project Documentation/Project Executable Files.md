# Project Executable Files

{{HEADER:3 Marks}}

## Step 1: Submission Checklist

| S.No | Item to Submit | Submitted (Yes / No / NA) |
|---|---|---|
| 1 | Complete source code (all files and folders) | Yes |
| 2 | README / Setup Guide (instructions to run the project) | Yes (`README.md`) |
| 3 | requirements.txt / package.json / dependency file | Yes (`requirements.txt`, `requirements-dev.txt`) |
| 4 | Database schema / seed files (if applicable) | NA (no database) |
| 5 | Environment configuration file (.env.example or similar) | Yes (`.env.example`) |
| 6 | Deployed application URL (if hosted) | NA (runs locally) |
| 7 | APK / Executable binary (if applicable for mobile/desktop apps) | NA (web application) |
| 8 | Dockerfile / Containerization config (if applicable) | Yes (`Dockerfile`, `.dockerignore`) |
| 9 | Test files and test results | Yes (`tests/`); results in `6.Project Testing/evidence/` once the team has run them |
| 10 | Demo video or walkthrough (if required) | {{demo_video_url}} |

## Step 2: File / Folder Structure

```
EduGenie/
|-- main.py                    FastAPI app: routes, validation, error handling
|-- gemini_utils.py            Gemini service: API key, model fallback, safe errors
|-- config.py                  Settings from environment variables
|-- models.py                  Pydantic request schema
|-- qna.py                     /qa  - question answering with follow-up context
|-- explanation_module.py      /explain - structured concept explanation
|-- quiz_module.py             /quiz - 3 MCQs as JSON, cleaned and validated
|-- summary_module.py          /summarize
|-- learning_path.py           /learn/recommendations
|-- check_gemini.py            Activity 1.3: Gemini connectivity check
|-- requirements.txt           Runtime dependencies
|-- requirements-dev.txt       Test and documentation tooling
|-- pytest.ini                 Test configuration
|-- .env.example               Environment template (copy to .env)
|-- Dockerfile, .dockerignore  Container build
|-- templates/                 index.html
|-- static/                    style.css, app.js
|-- tests/                     test_app.py, conftest.py, perf_load.py
|-- tools/                     build_docs.py, capture_screenshots.py
|-- docs-src/                  Editable Markdown sources and project.json for the PDFs
|-- 1. Brainstorming & Ideation/ ... 8.Project Demonstration/   Phase deliverables (PDF)
`-- README.md
```

## Step 3: Deployment / Access Details

| Field | Details |
|---|---|
| Hosted / Deployed URL | {{deployed_url}} |
| Login Credentials (Demo) | Not needed. EduGenie has no accounts. A Gemini API key is required in `.env` |
| Platform / Hosting Provider | Local Uvicorn server; Docker image available for Render, Railway, AWS or Azure |
| Repository Link | {{repo_url}} |
| Demo Video Link | {{demo_video_url}} |

## Step 4: Run Instructions

1. Install Python 3.10 or newer and Git.
2. `git clone {{repo_url}}` then `cd EduGenie`
3. Create and activate a virtual environment: `python -m venv venv` then `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux).
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and put your Gemini key from https://aistudio.google.com/apikey in `GEMINI_API_KEY`.
6. Optional check: `python check_gemini.py` (confirms Gemini access and shows which model works).
7. Start the server: `uvicorn main:app --reload` (or `python main.py`).
8. Open http://localhost:8000 and try each task. Interactive API docs are at http://localhost:8000/docs.
9. Run the tests: `pip install -r requirements-dev.txt` then `pytest tests`.
10. Docker alternative: `docker build -t edugenie .` then `docker run -p 8000:8000 --env-file .env edugenie`.

## Step 5: Known Issues / Limitations

| S.No | Known Issue / Limitation | Workaround / Status |
|---|---|---|
| 1 | AI answers can contain mistakes | Students should check important facts against their textbook; this is stated in the demo |
| 2 | A Gemini API key is required, and the free tier has usage limits | Create a free key in Google AI Studio; wait a moment if a "too many requests" message appears |
| 3 | Gemini model names change over time | Set `GEMINI_MODEL` in `.env`; the app also tries fallback models automatically |
| 4 | Follow-up context lives only in the open browser tab | Reloading the page starts a new conversation; saved history is planned |
| 5 | Text typed by the student is sent to the Google Gemini API | Do not enter private information |
