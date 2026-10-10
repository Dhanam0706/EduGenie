# EduGenie: Google Gemini Powered Learning Assistant

**Team ID:** SWTID-2026-2386

**AI/ML & GenAI Track project.** EduGenie is a lightweight AI learning assistant for students. Using Google Gemini it answers questions (with follow-ups), explains concepts, summarizes study material, generates quizzes and suggests learning paths, with a FastAPI backend and a simple HTML/CSS/JS page.

## Team

| Name | Register No. | Area |
|---|---|---|
| Dhanam V | 2024503505 | Prerequisites, setup, configuration, Gemini API (`config.py`, `gemini_utils.py`, `.env.example`, `check_gemini.py`) |
| Samyuktha B | 2024503581 | Core AI modules (`qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py`) |
| Sarumathi S | 2024503551 | Backend and API (`main.py`, `models.py`) |
| Risah Ruth R | 2024503543 | Frontend (`templates/`, `static/`) |
| Keerthana S | 2023503583 | Testing, documentation, demo (`tests/`, `tools/`, `docs-src/`, this README) |

Team details for the phase documents are set in `docs-src/project.json`; after editing it, run `python tools/build_docs.py`.

## Features

- **Ask a question**: concise, student-friendly answers, plus **follow-up questions** that use the previous answer as context.
- **Explain a concept**: definition, key ideas, a simple example and a common mistake.
- **Summarize text**: paste study notes and get the important points as short bullets.
- **Generate a quiz**: three multiple-choice questions with four options each; the page shows right/wrong instantly and reveals the correct answer.
- **Learning path**: Beginner, Intermediate and Advanced stages with time estimates and resources.
- **Reliability**: automatic Gemini model fallback chain, friendly error messages (empty input, invalid request, missing or rejected key, rate limit, network failure, bad quiz output) and no keys or stack traces shown.
- **Security**: the Gemini API key lives only in `.env` on the server and is never sent to the browser.

## Quick start

```bash
git clone https://github.com/Dhanam0706/EduGenie.git
cd EduGenie
python -m venv venv
venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           # macOS/Linux: cp .env.example .env
# edit .env: set GEMINI_API_KEY (https://aistudio.google.com/apikey)
python check_gemini.py           # optional: confirms Gemini works and picks a model
uvicorn main:app --reload
```

Open <http://localhost:8000>. Interactive API docs: <http://localhost:8000/docs>.
Without `GEMINI_API_KEY` the page loads, but each request shows a message asking you to add the key.

Docker: `docker build -t edugenie .` then `docker run -p 8000:8000 --env-file .env edugenie`.

## API

| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET | `/` | - | The web page |
| GET | `/health` | - | `{"status": "ok"}` |
| POST | `/qa` | `{"text": "...", "context": "optional previous answer"}` | `{"result": "..."}` |
| POST | `/explain` | `{"text": "..."}` | `{"result": "..."}` |
| POST | `/quiz` | `{"text": "..."}` | `{"questions": [{"question", "options", "answer_index"}]}` |
| POST | `/summarize` | `{"text": "..."}` | `{"result": "..."}` |
| POST | `/learn/recommendations` | `{"text": "..."}` | `{"result": "..."}` |

Errors return `{"detail": "friendly message"}` with status 400 (empty or too long input), 422 (invalid request), 429 (Gemini rate limit), 500 (missing key or unexpected error) or 502 (Gemini failure).

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests                      # Gemini is faked: no API key or internet needed
python tests/perf_load.py http://localhost:8000 25 20   # load test (server running; does not call Gemini)
```

Save the evidence for the Testing phase:

```bash
pytest tests -v > "6.Project Testing/evidence/pytest_results.txt"
python tests/perf_load.py http://localhost:8000 1 20  > "6.Project Testing/evidence/load_1_users.txt"
python tests/perf_load.py http://localhost:8000 10 20 > "6.Project Testing/evidence/load_10_users.txt"
python tests/perf_load.py http://localhost:8000 25 20 > "6.Project Testing/evidence/load_25_users.txt"
```

## Live demo script (about 8 minutes)

1. Run `python check_gemini.py`, then start the server and open the page.
2. **Ask a question**: `What is a Turing machine?`. Tick *follow-up* and ask `Can you give an example?`.
3. **Explain a concept**: `Operating system process synchronization`.
4. **Summarize text**: paste a paragraph of notes.
5. **Generate a quiz**: `The Pythagoras theorem`; click a wrong answer to show the correction.
6. **Learning path**: `SQL`.
7. Submit an empty box to show the friendly error message.
8. Run `pytest tests` in the terminal.

## Repository layout (follows the course template)

| Folder | Deliverables |
|---|---|
| `1. Brainstorming & Ideation` | Problem statements, empathy map, idea prioritization |
| `2. Requirement Analysis` | DFD, solution requirements, technology stack, customer journey map |
| `3. Project Design Phase` | Problem-solution fit, proposed solution, solution architecture |
| `4. Project Planning Phase` | Backlog, sprint schedule and estimation |
| `5. Project Development Phase` | Coding and solution, code layout, functional features (code is in the repo root) |
| `6.Project Testing` | Performance testing and raw evidence (pytest, load tests) |
| `7.Project Documentation` | Project executable files guide, full project documentation |
| `8.Project Demonstration` | Demo plan, team involvement, scalability, features, communication |

Application code: `main.py` (routes), `gemini_utils.py` (Gemini service), `config.py`, `models.py`, one module per feature (`qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py`), `templates/`, `static/`, `tests/`.

Editable sources for every phase PDF live in `docs-src/` (set team ID, names, dates and links in `docs-src/project.json`, then run `python tools/build_docs.py`).

## Note on the Gemini model

Earlier descriptions of this project name Gemini 1.5 Pro. That model family is retired, so set `GEMINI_MODEL` in `.env` (default `gemini-3.8-flash`); the app falls back to other current models automatically. Check the [current model list](https://ai.google.dev/gemini-api/docs/models) if a model is retired.
