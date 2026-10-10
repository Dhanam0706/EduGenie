# Performance Testing

{{HEADER:5 Marks}}

## Step 1: Testing Overview

| Field | Details |
|---|---|
| Testing Tool Used | Custom Python load script `tests/perf_load.py` (httpx + threads, psutil for CPU/RAM sampling); functional tests with pytest (`tests/test_app.py`) |
| Type of Testing | Load testing (1, 10 and 25 concurrent virtual users, 20 s each) and functional regression |
| Target Module / API | `GET /`, `GET /health` and `POST /qa` with empty text (rejected by validation before any Gemini call) |
| Test Environment | Linux cloud machine (1 vCPU, about 4 GB RAM, Python 3.12.3), single Uvicorn worker, load generator on the same machine. Gemini is deliberately **not** called, so the results measure EduGenie's own overhead and use no API quota |
| Test Date | {{date}} |

## Step 2: Test Scenarios

| S.No | Test Scenario / Description | No. of Virtual Users | Duration (sec) | Expected Outcome |
|---|---|---|---|---|
| 1 | Baseline: one user cycling through the three requests | 1 | 20 | Fast responses, 0 errors |
| 2 | Typical classroom load | 10 | 20 | Avg < 2 s, 0 errors |
| 3 | Peak load | 25 | 20 | Avg < 2 s, max < 5 s, error rate < 1 % |
| 4 | Functional regression under test (pytest) | 1 | - | All tests pass |

## Step 3: Performance Test Results (25 virtual users)

Measured by running `tests/perf_load.py` for 20 seconds with 25 virtual users (the raw output is in the `evidence` folder).

| S.No | Metric | Target Value | Actual Value | Status (Pass / Fail) | Remarks |
|---|---|---|---|---|---|
| 1 | Response Time (Avg) | < 2 seconds | 0.022 seconds | Pass | 95th percentile 0.029 s |
| 2 | Response Time (Max) | < 5 seconds | 0.177 seconds | Pass | Worst single request in 22,642 |
| 3 | Throughput (Req/sec) | Not specified | 1,130.8 req/s | N/A (no target set) | 22,642 requests in 20 s |
| 4 | Error Rate | < 1% | 0.00 % | Pass | No failed requests |
| 5 | CPU Utilization | < 80% | 42 % average (44 % peak) of one core | Pass | Shared with the load generator on the same single core, so the real server figure is lower |
| 6 | Memory Utilization | < 80% | 67 MB (about 1.7 % of 4 GB RAM) | Pass | Steady throughout the run |

### Results at each load level

| Virtual Users | Requests | Throughput (req/s) | Avg Response (s) | 95th Percentile (s) | Max Response (s) | Error Rate | CPU Avg | Memory |
|---|---|---|---|---|---|---|---|---|
| 1 | 22,010 | 1,099.9 | 0.001 | 0.001 | 0.007 | 0.00 % | 48 % | 67 MB |
| 10 | 24,025 | 1,200.2 | 0.008 | 0.011 | 0.034 | 0.00 % | 43 % | 67 MB |
| 25 | 22,642 | 1,130.8 | 0.022 | 0.029 | 0.177 | 0.00 % | 42 % | 67 MB |

### Functional tests (pytest)

32 tests ran and **32 passed** (0 failed) in 0.11 seconds.

## Step 4: Observations & Analysis

- All six metrics met their targets at 25 virtual users: average response 0.022 s (target < 2 s), maximum 0.177 s (target < 5 s) and 0 % errors (target < 1 %).
- Response time grows gently with load (0.001 s with 1 user, 0.008 s with 10 users, 0.022 s with 25 users) while throughput stays near 1,100 to 1,200 requests per second. The server is not saturated at this load.
- CPU stayed around 42 to 48 % of one core and memory stayed at about 67 MB at every load level, so EduGenie has plenty of headroom for a classroom-sized group.
- In normal use the response time is dominated by the Gemini call (typically a few seconds), not by EduGenie, which only validates the input and builds a prompt.
- The load test avoids Gemini on purpose: it keeps results repeatable and does not consume the free-tier quota. As a result, live Gemini latency was **not** measured by this test.
- The test used a single machine for both the server and the load generator, so absolute numbers will differ on other hardware. The commands in Step 5 can be re-run on any laptop.
- Scalability next steps: several Uvicorn workers, response caching and rate limiting (see Scalability & Future Plan).

## Step 5: Screenshots / Evidence

The raw output of every run is saved in the `6.Project Testing/evidence` folder:

| File | Contents |
|---|---|
| `load_1_users.txt` | Load test, 1 virtual user, 20 s |
| `load_10_users.txt` | Load test, 10 virtual users, 20 s |
| `load_25_users.txt` | Load test, 25 virtual users, 20 s |
| `pytest_results.txt` | Functional tests, 32 passed |

Output of the 25-user run:

```
virtual users      : 25
duration (s)       : 20.0
requests           : 22642
throughput (req/s) : 1130.8
avg response (s)   : 0.022
p95 response (s)   : 0.029
max response (s)   : 0.177
error rate (%)     : 0.00
server CPU avg/max : 42% / 44% (of one core)
server RSS avg/max : 67 MB / 67 MB
```

Output of the functional tests (last line): `32 passed, 1 warning in 0.11s`

To repeat the tests, run these from the project root:

```
uvicorn main:app --port 8000                       # terminal 1
python tests/perf_load.py http://localhost:8000 1 20  > "6.Project Testing/evidence/load_1_users.txt"
python tests/perf_load.py http://localhost:8000 10 20 > "6.Project Testing/evidence/load_10_users.txt"
python tests/perf_load.py http://localhost:8000 25 20 > "6.Project Testing/evidence/load_25_users.txt"
pytest tests -v > "6.Project Testing/evidence/pytest_results.txt"
```

Functional tests cover: a valid question, follow-up context, empty / invalid / too-long input on every endpoint, summary, quiz generation (including code fences and bad Gemini output), Gemini failure with hidden details, empty Gemini reply, missing key, rejected key, model fallback, rate limit, hidden unexpected errors, and the page-to-API round trip.
