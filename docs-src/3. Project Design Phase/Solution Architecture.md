# Solution Architecture

{{HEADER:5 Marks}}

## Solution Architecture Diagram

```
                          Presentation / Client Layer
        Browser: HTML + CSS + JavaScript (one Jinja2 page: task dropdown, text area,
        submit button, result area, quiz buttons)
                                        |  ^
                          HTTP/JSON     v  |
                              API Layer (FastAPI + Uvicorn)
        Routes: /  /health  /qa  /explain  /quiz  /summarize  /learn/recommendations
        Request validation (Pydantic), input limits, friendly exception handlers
                                        |  ^
        +-------------------------------+--+--------------------------------+
        v                               v                                   v
  Feature modules                  Gemini service                      External API
  [qna.py, explanation_module.py,  [gemini_utils.py: reads the key     [Google Gemini API
   quiz_module.py (JSON parse and   from config, calls Gemini with       (text)]
   validation), summary_module.py,  model fallback, turns failures
   learning_path.py: build prompts] into safe error messages]
                        |
                        v
              Configuration: config.py + .env (GEMINI_API_KEY, GEMINI_MODEL)
              No database: the service is stateless
```

## Component Description Table

| Component Name | Description / Role in Architecture | Technologies Used |
|---|---|---|
| Presentation Layer | One responsive page: choose a task, type input, read the result, answer quiz questions with instant feedback | HTML5, CSS3, JavaScript, Jinja2 |
| API Layer (`main.py`) | Routing, validation, input limits and friendly error handling; one endpoint per feature, plus `/health` | FastAPI, Uvicorn, Pydantic |
| Models (`models.py`) | Request schema shared by every endpoint | Pydantic |
| Feature modules | One file per feature builds the prompt: `qna.py`, `explanation_module.py`, `summary_module.py`, `quiz_module.py` (also cleans and validates the JSON), `learning_path.py` | Python |
| Gemini service (`gemini_utils.py`) | Calls Gemini, tries fallback models if one is retired or busy, and converts failures into messages that are safe to show | google-genai |
| Configuration (`config.py`) | Reads the API key, model name, timeouts and limits from environment variables | python-dotenv |
| External APIs | Google Gemini for all generated content | Google Gemini API |
