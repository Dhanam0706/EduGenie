# EduGenie: Google Gemini Powered Learning Assistant

**Team ID:** {{team_id}}

## Project Description

EduGenie is a lightweight AI-powered educational assistant that simplifies learning with Google Gemini. A FastAPI backend validates the student's input, builds a task-specific prompt and sends it to Gemini. The page then shows the answer, explanation, summary, quiz or learning path. Designed for students of all levels, EduGenie lets users:

* Ask questions and receive smart, concise answers, with follow-up questions
* Understand complex concepts through simplified, structured explanations
* Generate quizzes from topics or text
* Summarize large educational passages
* Receive a personalised learning path from beginner to advanced

## Scenarios

**Scenario 1: Asking a question.** A student wants to know about oceans and rivers and asks "Which is the largest ocean?". EduGenie answers in a short, clear paragraph, and the student can tick "follow-up" and ask for an example.

**Scenario 2: Testing understanding.** A student wants to know how well she understands "The Pythagoras Theorem" and chooses *Generate a quiz*. EduGenie shows three multiple-choice questions. A wrong choice turns red and the correct answer is shown in green.

**Scenario 3: Learning path.** A learner exploring SQL requests a learning path. EduGenie returns a structured plan with beginner, intermediate and advanced stages, timelines and resource suggestions.

## Technical Architecture

Three parts: a responsive HTML/CSS/JS page (one Jinja2 template), a FastAPI back end (routes, validation, feature modules and one shared Gemini service) and the external Google Gemini API. There is no database. See *3. Project Design Phase / Solution Architecture* for the diagram.

## Pre-requisites

1. Python 3.10+ - https://www.python.org
2. FastAPI - https://fastapi.tiangolo.com
3. Google AI Studio account and Gemini API key - https://aistudio.google.com/apikey
4. Git and a GitHub account
5. Basic HTML, CSS and JavaScript

## Project Workflow

| Milestone | Activities | Where in the code |
|---|---|---|
| 1. Gemini AI Initialization | 1.1 Create Google AI Studio account; 1.2 generate and store the API key in `.env`; 1.3 validate connectivity and pick a working model | `.env.example`, `config.py`, `check_gemini.py` |
| 2. Core Functionalities Development | 2.1 Explanation; 2.2 Question answering with follow-ups; 2.3 Quiz generation with JSON cleaning and validation; 2.4 Summarization; 2.5 Learning path | `explanation_module.py`, `qna.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py`, `gemini_utils.py` |
| 3. Backend - FastAPI Integration | 3.1 One endpoint per module: `/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`; 3.2 input validation and friendly errors; 3.3 `/health` and `__main__` | `main.py`, `models.py` |
| 4. UI Development | 4.1 Task dropdown, text area, submit button; 4.2 result area, loading message, quiz buttons | `templates/index.html`, `static/` |
| 5. Testing & Optimization | 5.1 Automated tests with a fake Gemini; 5.2 load test; 5.3 prompt tuning; 5.4 error and fallback handling | `tests/`, `gemini_utils.py` |

## Milestone 1: Gemini AI Initialization

1. Sign in at https://aistudio.google.com and choose **Get API key** then **Create API key**.
2. Copy the key into `.env` as `GEMINI_API_KEY` (never commit `.env`).
3. Run `python check_gemini.py`. It sends a short prompt, tries the configured model and then the fallback models, and prints which model to use.

Note: earlier descriptions of this project mention Gemini 1.5 Pro. That model family is retired, so the model is configurable (`GEMINI_MODEL`).

## Milestone 2 and 3: Core Modules and Backend

- **Explanation module.** Asks Gemini for a definition, key ideas, a simple example and one common mistake, in beginner-friendly language.
- **QnA module.** Answers academic questions concisely. For a follow-up, the previous question and answer are added to the prompt as context.
- **Quiz module.** Asks for exactly three multiple-choice questions with four options and one correct answer, as JSON. `clean_json_block` removes Markdown code fences, the JSON is parsed and every question is checked (four options, answer present). A bad reply gives a friendly message instead of a broken quiz.
- **Summary module.** Turns long text into short bullet points that keep key terms and add nothing new.
- **Learning path module.** Builds Beginner, Intermediate and Advanced stages with time estimates and resource types.
- `gemini_utils.py` makes the Gemini call, tries fallback models when the chosen one is retired or busy, and converts every failure into a message that is safe to show.
- `main.py` exposes `/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`, `/health` and the page `/`. Interactive API docs are at `/docs`.

## Milestone 4: UI Development

![Home page](assets/01_home.png)

The student chooses a task, types a topic or pastes notes, and presses Submit. The result appears below the form.

## Milestone 5: Testing & Optimization

### Explanation

![Explain a concept](assets/04_explain.png)

### Summarization

![Summary](assets/05_summary.png)

### Learning path

![Learning path](assets/07_learning_path.png)

### Error handling

![Error message shown when Gemini cannot complete a request](assets/08_error_message.png)

When Gemini fails, the app shows a short, safe message and no technical details.

## Conclusion

EduGenie combines FastAPI with Google Gemini to make learning simpler. It answers questions, explains concepts, summarises notes, quizzes the student and suggests what to learn next, while keeping the API key on the server and showing friendly messages when something goes wrong. Its modular design, with one file per feature, keeps it easy to understand, test and extend.
