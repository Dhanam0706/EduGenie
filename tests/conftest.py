"""Test setup: no Gemini key (so a real .env is never used and no real call can happen).

Every test that needs Gemini replaces it with a fake, so no API key or internet is needed.
"""
import os

# Set before the app is imported: python-dotenv never overrides variables that already exist.
os.environ["GEMINI_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as c:
        yield c
