"""EduGenie automated tests. Gemini is always faked, so no API key or internet is needed.

Run from the project root:  pytest tests
Save the evidence:          pytest tests -v > "6.Project Testing/evidence/pytest_results.txt"
"""
import json

import pytest
from google.genai import errors as genai_errors

import config
import gemini_utils
import main

QUIZ_JSON = json.dumps(
    [
        {"question": f"Question {i}?", "options": ["One", "Two", "Three", "Four"], "answer": "B"}
        for i in range(1, 4)
    ]
)
ENDPOINTS = ["/qa", "/explain", "/quiz", "/summarize", "/learn/recommendations"]


# ----------------------------------------------------------------- helpers

def fake_generate(reply):
    """Replacement for gemini_utils.generate that returns a fixed reply and records the prompts."""
    prompts = []

    def _fake(prompt):
        prompts.append(prompt)
        return reply

    _fake.prompts = prompts
    return _fake


class FakeAPIError(genai_errors.APIError):
    """APIError built without the SDK constructor, so the tests do not depend on its signature."""

    def __init__(self, code, message="boom"):
        Exception.__init__(self, message)
        self.code = code
        self.message = message


def install_fake_client(monkeypatch, behaviour):
    """Fake google-genai client. behaviour(model) returns the reply text or raises."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    models_called = []

    class FakeModels:
        def generate_content(self, model, contents):
            models_called.append(model)
            return type("Response", (), {"text": behaviour(model)})()

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.models = FakeModels()

    monkeypatch.setattr(gemini_utils.genai, "Client", FakeClient)
    return models_called


# ----------------------------------------------------------------- pages and frontend/backend communication

def test_home_page_has_form_and_hides_key(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text
    assert "<form" in response.text
    assert "/static/app.js" in response.text
    assert "GEMINI_API_KEY" not in response.text


def test_static_files_are_served(client):
    css = client.get("/static/style.css")
    js = client.get("/static/app.js")
    assert css.status_code == 200 and "text/css" in css.headers["content-type"]
    assert js.status_code == 200
    for path in ENDPOINTS:  # the frontend script knows every backend endpoint
        assert path in js.text


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_frontend_to_backend_round_trip(client, monkeypatch):
    """The frontend sends JSON {text, context} and reads {result} back."""
    monkeypatch.setattr(gemini_utils, "generate", fake_generate("Binary search example."))
    response = client.post(
        "/explain",
        json={"text": "Explain binary search with an example.", "context": ""},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {"result": "Binary search example."}


# ----------------------------------------------------------------- valid requests

def test_valid_question(client, monkeypatch):
    fake = fake_generate("A Turing machine is a model of computation.")
    monkeypatch.setattr(gemini_utils, "generate", fake)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 200
    assert "Turing machine" in response.json()["result"]
    assert "What is a Turing machine?" in fake.prompts[0]


def test_follow_up_question_sends_context(client, monkeypatch):
    fake = fake_generate("Sure, here is more detail.")
    monkeypatch.setattr(gemini_utils, "generate", fake)
    response = client.post(
        "/qa",
        json={"text": "Can you give an example?", "context": "EduGenie answered: Binary search halves the range."},
    )
    assert response.status_code == 200
    assert "Binary search halves the range" in fake.prompts[0]


@pytest.mark.parametrize("path", ["/explain", "/learn/recommendations", "/summarize"])
def test_text_endpoints_return_result(client, monkeypatch, path):
    monkeypatch.setattr(gemini_utils, "generate", fake_generate("some answer"))
    response = client.post(path, json={"text": "Process synchronization"})
    assert response.status_code == 200
    assert response.json() == {"result": "some answer"}


def test_summary_request(client, monkeypatch):
    fake = fake_generate("- Point one\n- Point two")
    monkeypatch.setattr(gemini_utils, "generate", fake)
    response = client.post("/summarize", json={"text": "A long paragraph about photosynthesis."})
    assert response.status_code == 200
    assert "Point one" in response.json()["result"]
    assert "photosynthesis" in fake.prompts[0]


# ----------------------------------------------------------------- input validation

@pytest.mark.parametrize("path", ENDPOINTS)
def test_empty_input_is_rejected(client, path):
    response = client.post(path, json={"text": "   "})
    assert response.status_code == 400
    assert "enter" in response.json()["detail"].lower()


def test_invalid_request_is_rejected(client):
    response = client.post("/qa", json={"wrong_field": "hello"})
    assert response.status_code == 422
    assert "Invalid request" in response.json()["detail"]


def test_too_long_input_is_rejected(client):
    response = client.post("/summarize", json={"text": "a" * (config.MAX_INPUT_CHARS + 1)})
    assert response.status_code == 400
    assert "too long" in response.json()["detail"]


# ----------------------------------------------------------------- quiz generation

def test_quiz_generation(client, monkeypatch):
    monkeypatch.setattr(gemini_utils, "generate", fake_generate(QUIZ_JSON))
    response = client.post("/quiz", json={"text": "Pythagoras theorem"})
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) == 3
    assert len(questions[0]["options"]) == 4
    assert questions[0]["answer_index"] == 1


def test_quiz_handles_markdown_fences(client, monkeypatch):
    monkeypatch.setattr(gemini_utils, "generate", fake_generate("```json\n" + QUIZ_JSON + "\n```"))
    response = client.post("/quiz", json={"text": "Pythagoras theorem"})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 3


def test_quiz_answer_can_be_option_text(client, monkeypatch):
    data = [{"question": "Q?", "options": ["a", "b", "c", "d"], "answer": "c"}]
    monkeypatch.setattr(gemini_utils, "generate", fake_generate(json.dumps(data)))
    response = client.post("/quiz", json={"text": "anything"})
    assert response.status_code == 200
    assert response.json()["questions"][0]["answer_index"] == 2


@pytest.mark.parametrize(
    "bad_reply",
    [
        "Sorry, I cannot make a quiz.",                                                # not JSON
        "[]",                                                                          # no questions
        json.dumps([{"question": "Q?", "options": ["a", "b"], "answer": "A"}]),        # too few options
        json.dumps([{"question": "Q?", "options": ["a", "b", "c", "d"], "answer": "Z"}]),  # answer not in options
    ],
)
def test_quiz_with_unexpected_response(client, monkeypatch, bad_reply):
    monkeypatch.setattr(gemini_utils, "generate", fake_generate(bad_reply))
    response = client.post("/quiz", json={"text": "Pythagoras theorem"})
    assert response.status_code == 502
    assert "valid quiz" in response.json()["detail"]


# ----------------------------------------------------------------- Gemini failures and API key

def test_missing_api_key(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 500
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_gemini_api_failure_hides_details(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")

    class BrokenClient:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("secret internal details")

    monkeypatch.setattr(gemini_utils.genai, "Client", BrokenClient)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 502
    detail = response.json()["detail"]
    assert "Could not reach Gemini" in detail
    assert "secret internal details" not in detail
    assert "test-key-123" not in detail


def test_empty_gemini_response(client, monkeypatch):
    install_fake_client(monkeypatch, lambda model: "")
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 502
    assert "empty answer" in response.json()["detail"]


def test_rejected_api_key_stops_the_chain(client, monkeypatch):
    def behaviour(model):
        raise FakeAPIError(403, "permission denied")

    models_called = install_fake_client(monkeypatch, behaviour)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 502
    assert "API key was rejected" in response.json()["detail"]
    assert len(models_called) == 1  # a bad key would fail on every model, so it stops at once


def test_model_chain_falls_through_to_next_model(client, monkeypatch):
    def behaviour(model):
        if model == config.get_model():
            raise FakeAPIError(404, "model not found")
        return "answer from the fallback model"

    models_called = install_fake_client(monkeypatch, behaviour)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 200
    assert response.json()["result"] == "answer from the fallback model"
    assert len(models_called) == 2


def test_all_models_rate_limited(client, monkeypatch):
    def behaviour(model):
        raise FakeAPIError(429, "quota")

    models_called = install_fake_client(monkeypatch, behaviour)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 429
    assert "too many requests" in response.json()["detail"]
    assert len(models_called) == len(gemini_utils._model_chain())


def test_model_chain_has_no_duplicates(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", config.GEMINI_FALLBACK_MODELS[0])
    chain = gemini_utils._model_chain()
    assert chain[0] == config.GEMINI_FALLBACK_MODELS[0]
    assert len(chain) == len(set(chain))
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert gemini_utils._model_chain()[0] == config.DEFAULT_MODEL


def test_unexpected_error_is_hidden(client, monkeypatch):
    def broken(*args):
        raise ValueError("stack trace details")

    monkeypatch.setattr(main, "answer_question", broken)
    response = client.post("/qa", json={"text": "What is a Turing machine?"})
    assert response.status_code == 500
    assert "stack trace details" not in response.json()["detail"]
    assert "unexpected" in response.json()["detail"].lower()
