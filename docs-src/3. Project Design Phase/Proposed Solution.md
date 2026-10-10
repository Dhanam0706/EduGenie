# Project Initialization and Planning Phase

{{HEADER:5 Marks}}

## Project Proposal (Proposed Solution) report

EduGenie is a lightweight, GenAI-powered learning assistant. It turns a student's question, topic or study notes into a clear answer, a structured explanation, a summary, a quiz or a learning path.

### Project Overview
| | |
|---|---|
| Objective | Help students understand, revise and test academic topics using Google Gemini, in a simple web page focused on learning |
| Scope | Five features (question answering with follow-ups, concept explanation, summarization, quiz generation, learning path); no accounts, no database, no file uploads |

### Problem Statement
| | |
|---|---|
| Description | Students find explanations too complex, notes too long to revise and practice questions hard to get for their own topic |
| Impact | Solving this saves study time, improves understanding and helps students check their own progress |

### Proposed Solution
| | |
|---|---|
| Approach | A FastAPI backend validates the student's input, a feature module builds a task-specific prompt, and one shared Gemini service sends it (with an automatic model fallback) and returns the result. The quiz reply is requested as JSON, cleaned, parsed and validated before it reaches the page. The API key stays on the server |
| Key Features | - Ask a question, with optional follow-ups<br>- Structured concept explanations with an example<br>- Summaries of pasted study notes<br>- Three-question quiz with instant feedback and corrected answers<br>- Learning path from beginner to advanced<br>- Friendly error messages and key protection |

### Resource Requirements
| Resource Type | Description | Specification / Allocation |
|---|---|---|
| **Hardware** | | |
| Computing Resources | CPU/GPU specifications, number of cores | Any laptop, no GPU (inference runs in Google's cloud) |
| Memory | RAM specifications | 4 GB minimum; the server itself is small |
| Storage | Disk space for data, models and logs | Under 1 GB; no model download and no database |
| **Software** | | |
| Frameworks | Python frameworks | FastAPI, Uvicorn, Jinja2 |
| Libraries | Additional libraries | google-genai, pydantic, python-dotenv, pytest |
| Development Environment | IDE | VS Code, Git, GitHub |
| **Data** | | |
| Data | Source, size, format | No training dataset; the student's text at run time (JSON) and Gemini responses (text or JSON). Nothing is stored |
