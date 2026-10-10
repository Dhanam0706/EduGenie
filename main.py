"""EduGenie: Google Gemini Powered Learning Assistant - FastAPI app.

Run with:  uvicorn main:app --reload
Open:      http://127.0.0.1:8000        Interactive API docs: http://127.0.0.1:8000/docs

Each endpoint validates the input and calls the matching module.

Depends on: config.py, models.py, gemini_utils.py, qna.py, explanation_module.py,
            quiz_module.py, summary_module.py, learning_path.py, templates/, static/
"""
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import config
from explanation_module import explain_concept
from gemini_utils import GeminiError
from learning_path import get_learning_recommendations
from models import UserRequest
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

logger = logging.getLogger("edugenie")

app = FastAPI(title="EduGenie: Google Gemini Powered Learning Assistant")
app.mount("/static", StaticFiles(directory=config.BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(config.BASE_DIR / "templates"))


# ---------- error handling ----------

@app.exception_handler(GeminiError)
async def gemini_error_handler(request: Request, exc: GeminiError):
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request. Please send your text as a string in the 'text' field."},
    )


def _validated_text(body: UserRequest) -> str:
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter a question or topic first.")
    if len(text) > config.MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Your input is too long. Please keep it under {config.MAX_INPUT_CHARS} characters.",
        )
    return text


def _run(func, *args):
    """Call a module function; hide unexpected errors behind a friendly message."""
    try:
        return func(*args)
    except GeminiError:
        raise
    except Exception:
        logger.exception("Unexpected error in %s", getattr(func, "__name__", "module"))
        raise GeminiError("Something unexpected went wrong. Please try again.", status_code=500)


# ---------- pages ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------- API endpoints (one per module) ----------

@app.post("/qa")
async def qa(body: UserRequest):
    text = _validated_text(body)
    return {"result": _run(answer_question, text, body.context[: config.MAX_INPUT_CHARS])}


@app.post("/explain")
async def explain(body: UserRequest):
    text = _validated_text(body)
    return {"result": _run(explain_concept, text)}


@app.post("/quiz")
async def quiz(body: UserRequest):
    text = _validated_text(body)
    return {"questions": _run(generate_quiz, text)}


@app.post("/summarize")
async def summarize(body: UserRequest):
    text = _validated_text(body)
    return {"result": _run(summarize_text, text)}


@app.post("/learn/recommendations")
async def learn_recommendations(body: UserRequest):
    text = _validated_text(body)
    return {"result": _run(get_learning_recommendations, text)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
