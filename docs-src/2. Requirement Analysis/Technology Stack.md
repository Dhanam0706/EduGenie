# Technology Stack

{{HEADER:2 Marks}}

## Technology Stack Details

| S.No | Architecture Component / Layer | Technology Chosen | Justification / Purpose |
|---|---|---|---|
| 1 | Frontend / Client-Side | HTML5, CSS3, vanilla JavaScript, Jinja2 template | No build step and fast to load; AI text is rendered with `textContent` to prevent injection; responsive on phones |
| 2 | Backend / Server-Side | Python 3, FastAPI, Uvicorn, Pydantic | Simple, automatic request validation and API docs at `/docs`; easy for the whole team to read |
| 3 | Database / Data Storage | None | EduGenie is stateless; nothing is stored. A database is listed as a future enhancement (progress tracking) |
| 4 | Cloud / Hosting / Deployment | Local Uvicorn server, Docker (`Dockerfile` provided) | Simple to run for the demo; the container image can be deployed to Render, Railway or any cloud VM |
| 5 | Version Control & CI/CD | Git and GitHub, pytest | Collaboration for five members; automated test suite ready to plug into GitHub Actions |
| 6 | Third-Party APIs / Other Tools | Google Gemini API (`google-genai` SDK), python-dotenv | Gemini generates answers, explanations, summaries, quizzes and learning paths; dotenv keeps the key out of the code |
