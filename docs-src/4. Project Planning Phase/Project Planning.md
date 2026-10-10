# Initial Project Planning Template

{{HEADER:5 Marks}}

## Product Backlog, Sprint Schedule, and Estimation (4 Marks)

| Sprint | Functional Requirement (Epic) | User Story Number | User Story / Task | Story Points | Priority | Team Members | Sprint Start Date | Sprint End Date (Planned) |
|---|---|---|---|---|---|---|---|---|
| Sprint-1 | Gemini setup | USN-1 | As a developer, I can call Gemini using an API key stored in `.env`, and check it with `check_gemini.py` | 2 | High | {{member1}} | {{s1_start}} | {{s1_end}} |
| Sprint-1 | Backend skeleton | USN-2 | As a developer, I have a FastAPI app with configuration, request model and a health check | 3 | High | {{member3}}, {{member1}} | {{s1_start}} | {{s1_end}} |
| Sprint-1 | Frontend base | USN-3 | As a student, I see one page with a task dropdown, text area and submit button | 3 | High | {{member4}} | {{s1_start}} | {{s1_end}} |
| Sprint-2 | Question answering | USN-4 | As a student, I can ask a question and then ask follow-up questions on the last answer | 3 | High | {{member2}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | Concept explanation | USN-5 | As a student, I get a structured explanation with an example | 2 | High | {{member2}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | Summarization | USN-6 | As a student, I can paste notes and get the key points | 2 | High | {{member2}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | Quiz generation | USN-7 | As a student, I can generate a three-question quiz from a topic or notes and see which answers are right or wrong | 5 | High | {{member2}}, {{member4}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | Learning path | USN-8 | As a student, I get a beginner-to-advanced plan with resources | 2 | Medium | {{member2}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | API endpoints | USN-9 | As a developer, each feature is reachable through its own endpoint with input validation | 3 | High | {{member3}} | {{s2_start}} | {{s2_end}} |
| Sprint-2 | Results interface | USN-10 | As a student, I see the answer below the form, a loading message and quiz buttons | 3 | High | {{member4}} | {{s2_start}} | {{s2_end}} |
| Sprint-3 | Reliability and errors | USN-11 | As a student, I always get a clear message if the input is empty, the key is missing or Gemini fails, and the app tries other models | 3 | High | {{member1}}, {{member3}} | {{s3_start}} | {{s3_end}} |
| Sprint-3 | Testing | USN-12 | As a team, we verify every feature with automated tests that fake Gemini, plus a load test | 5 | High | {{member5}} | {{s3_start}} | {{s3_end}} |
| Sprint-3 | Documentation and demo | USN-13 | As an evaluator, I can run the project from the README and see all phase documents | 3 | Medium | {{member5}} | {{s3_start}} | {{s3_end}} |

### Sprint Summary

| Sprint | Total Story Points | Duration | Velocity (points / day) |
|---|---|---|---|
| Sprint-1 | 8 | 2 days | 4.0 |
| Sprint-2 | 20 | 3 days | 6.7 |
| Sprint-3 | 11 | 1 day | 11.0 |
| **Total** | **39** | 6 days | **6.5 average** |
