# Project Demo Planning

{{HEADER:1 Mark}}

## Project Demo Planning

| S.No | Demo Section | Description | Duration (mins) | Responsible Member |
|---|---|---|---|---|
| 1 | Introduction & problem statement | Why students need simple explanations, summaries and practice; project goal | 1 | {{member5}} |
| 2 | Architecture & tech stack | FastAPI + Gemini diagram; one module per feature; model fallback | 2 | {{member3}} |
| 3 | Setup and Gemini key | `.env`, `check_gemini.py`, why the key never reaches the browser | 1 | {{member1}} |
| 4 | Question, follow-up, explanation (live) | Ask "What is a Turing machine?", then a follow-up; explain process synchronization | 2 | {{member2}} |
| 5 | Summary and quiz (live) | Summarize pasted notes; quiz on the Pythagoras theorem, choose a wrong answer | 2 | {{member4}} |
| 6 | Learning path, errors and testing | SQL learning path; empty input message; run `pytest` | 2 | {{member5}} |
| 7 | Scalability, future plan, Q&A | Roadmap and answers | 2 | Whole team |

### Demo Flow Summary

| Step | Activity | Notes |
|---|---|---|
| 1 | Introduction & Problem Statement | Use PS-1 to PS-4 from Phase 1 |
| 2 | Solution Overview | Show the architecture diagram and the one-file-per-feature layout |
| 3 | Live Feature Demonstration | Question, follow-up, explanation, summary, quiz (pick a wrong answer), learning path, empty-input message |
| 4 | Q&A Session | Be ready to explain the model fallback, quiz JSON validation and where the API key is kept |

### Pre-demo checklist
- `.env` has a working `GEMINI_API_KEY`; run `python check_gemini.py` the day before.
- Server started with `uvicorn main:app`; page opened at http://localhost:8000.
- Prepare a paragraph of notes to paste into Summarize.
- Run `pytest tests` once and keep the result ready to show.
- If Wi-Fi fails, the app cannot reach Gemini and shows a friendly message; explain this as the expected behaviour.
