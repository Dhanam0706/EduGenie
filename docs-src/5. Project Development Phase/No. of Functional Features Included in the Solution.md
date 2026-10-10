# No. of Functional Features Included in the Solution

{{HEADER:5 Marks}}

## Functional Features Overview

| S.No | Feature Name | Feature Description | Module / Component | Status (Done / In Progress / Pending) | Marks Contribution |
|---|---|---|---|---|---|
| 1 | Ask a question | Educational answer to any academic question | `qna.py`, `/qa` | Done | Core |
| 2 | Follow-up questions | The previous question and answer are sent as context for the next question | `qna.py`, `app.js` | Done | Core |
| 3 | Concept explanation | Definition, key ideas, example and common mistake | `explanation_module.py`, `/explain` | Done | Core |
| 4 | Summarization | Key points from pasted study material | `summary_module.py`, `/summarize` | Done | Core |
| 5 | Quiz generation | Three multiple-choice questions with four options; JSON cleaned and validated | `quiz_module.py`, `/quiz` | Done | Core |
| 6 | Quiz feedback | Chosen option turns green or red and the correct answer is shown | `app.js`, `style.css` | Done | Core |
| 7 | Learning path | Beginner to advanced stages with time estimates and resources | `learning_path.py`, `/learn/recommendations` | Done | Core |
| 8 | Input validation | Empty, too long (over 8000 characters) and malformed requests are rejected | `main.py`, `models.py` | Done | Core |
| 9 | Friendly error handling | Missing key, rejected key, rate limit, network failure, empty or invalid Gemini reply | `gemini_utils.py`, `main.py` | Done | Core |
| 10 | Gemini model fallback | Tries other models if the chosen model is retired or busy | `gemini_utils.py`, `config.py` | Done | Additional |
| 11 | API key protection | Key only in `.env`, read on the server, `.env` ignored by git | `config.py`, `.gitignore` | Done | Core |
| 12 | Health check and Docker | `/health` endpoint and a Dockerfile | `main.py`, `Dockerfile` | Done | Additional |

### Feature Summary

| Metric | Count / Value |
|---|---|
| Total Features Planned | 12 |
| Total Features Implemented | 12 |
| Core / Must-Have Features | 10 |
| Additional / Nice-to-Have Features | 2 |
| Features Tested & Verified | Automated tests exist for every feature (`tests/test_app.py`); the team records the run in `6.Project Testing/evidence/pytest_results.txt` |

### Feature Category Breakdown

| S.No | Category | Features in Category | Example Features |
|---|---|---|---|
| 1 | User Interface (UI) | 2 | Follow-up questions, quiz feedback |
| 2 | Backend / Logic | 4 | Question answering, explanation, summary, learning path |
| 3 | Database / Storage | 0 | Not used (stateless) |
| 4 | API / Integration | 3 | Quiz generation (Gemini JSON), model fallback, health check and Docker |
| 5 | Security / Authentication | 3 | Input validation, friendly error handling, API key protection |
