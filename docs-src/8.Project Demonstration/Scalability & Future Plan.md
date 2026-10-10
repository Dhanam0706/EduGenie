# Scalability & Future Plan

{{HEADER:1 Mark}}

## Current System Limitations

| S.No | Limitation | Impact | Priority to Address (High / Medium / Low) |
|---|---|---|---|
| 1 | No saved history or user accounts | Students lose their answers when they close the page | Medium |
| 2 | Free-tier Gemini limits and AI latency | Slow or rate-limited replies when many students use it at once | High |
| 3 | Text only; no voice, files or images | Students cannot upload a PDF or a photo of a problem | Medium |

## Scalability Plan

| S.No | Scalability Aspect | Current State | Proposed Upgrade / Solution |
|---|---|---|---|
| 1 | User Load | Single worker; stateless, so more workers can be added | Several Uvicorn/Gunicorn workers behind Nginx; container autoscaling |
| 2 | Data Storage | None | PostgreSQL for accounts, history and quiz scores |
| 3 | Performance | One Gemini call per request | Cache repeated questions, use the async Gemini client, rate-limit each user |
| 4 | Security | Key in `.env`, input limits, safe error messages | Secrets manager, HTTPS-only deployment, per-user rate limiting |

## Future Roadmap

| Phase | Planned Feature / Enhancement | Target Timeline | Expected Impact |
|---|---|---|---|
| Phase 2 | Voice input and output, multilingual support | 1-2 months | More accessible to learners in different languages |
| Phase 3 | Progress tracking dashboard, badges, learning streaks, adaptive learning paths | 2-3 months | More engagement and personalised practice |
| Phase 4 | PDF and image input, mobile app, teacher/parent dashboards, LMS integration (Moodle, Google Classroom) | 3-6 months | Wider reach inside schools and colleges |
