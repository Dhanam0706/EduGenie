# Solution Requirements

{{HEADER:4 Marks}}

## Step 1: Functional Requirements (FR)

| S.No | Requirement Category | Requirement Description | Priority |
|---|---|---|---|
| 1 | Authentication | Not required. EduGenie is an open learning tool with no accounts; no personal data is collected | Low |
| 2 | Authorization levels | Single role (student). The Gemini API key is held only by the server and is never sent to the browser | High |
| 3 | External interfaces | Google Gemini API (text) through the `google-genai` SDK | High |
| 4 | Transactions processing | Each request is validated, turned into a prompt, sent to Gemini and the result returned. Nothing is stored | High |
| 5 | Reporting | Formatted answers, explanations, summaries and learning paths; a three-question quiz with instant right/wrong feedback and the correct answer shown | High |
| 6 | Business rules | Input must not be empty and is limited to 8000 characters; a quiz has exactly 3 multiple-choice questions with 4 options and one correct answer; answers stay educational | High |
| 7 | Compliance to laws or regulations | API key kept in `.env` and never committed; no personal data is stored; text typed by the student is sent to the Google Gemini API, so students should not enter private information | Medium |
| 8 | Other | Automatic model fallback if the chosen Gemini model is unavailable; friendly error messages with no keys or stack traces | High |

## Step 2: Non-Functional Requirements (NFR)

| S.No | NFR Category | Requirement Description | Target Metric / Acceptance Criteria |
|---|---|---|---|
| 1 | Performance & Speed | EduGenie's own processing is small; Gemini latency dominates | Avg app response < 2 s and max < 5 s for requests that do not call Gemini (measured with `tests/perf_load.py`) |
| 2 | Scalability | Stateless request handling, so more Uvicorn workers can be added; no database to share | 25 concurrent users with < 1 % errors on non-Gemini requests |
| 3 | Security & Data Privacy | API key in `.env`, never in code or browser; AI text shown with `textContent` so it cannot inject HTML; no stack traces shown | No key in the repository or in any response; all errors return a friendly message |
| 4 | Reliability & Availability | Falls back through several Gemini models; clear message if Gemini is unreachable | A retired or busy model does not stop the app while another listed model works |
| 5 | Usability & Accessibility | One simple page; labelled fields; responsive layout | Usable at 360 px width; keyboard navigable |
| 6 | Other | Maintainability and portability: one module per feature, `.env` configuration, Dockerfile | Runs with `pip install -r requirements.txt` and `uvicorn main:app` |
