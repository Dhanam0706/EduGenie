"""Concept explanation module.

The Common Template used a local LaMini-Flan-T5 model here. EduGenie uses Gemini
instead so the project needs no heavy local model (torch/transformers).

Depends on: gemini_utils.py
"""

import gemini_utils


def explain_concept(topic: str) -> str:
    """Explain a concept in simple, structured language."""
    prompt = (
        "You are EduGenie, a friendly teacher. Explain the topic below to a student "
        "who is new to it.\n"
        "Use this structure:\n"
        "1. A one or two sentence plain-language definition.\n"
        "2. The key ideas as short bullet points.\n"
        "3. A simple example.\n"
        "4. One common mistake or thing to remember.\n"
        "Keep it concise but detailed enough to understand.\n\n"
        f"Topic: {topic}"
    )
    return gemini_utils.generate(prompt)
