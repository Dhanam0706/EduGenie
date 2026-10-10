"""Simple load test (threads + httpx) with CPU/memory sampling.

Measures EduGenie's own overhead WITHOUT calling Gemini: the home page, /health and a
request with empty text (rejected by validation before any Gemini call). Results therefore
exclude Gemini latency and use none of your API quota. Usage:
    uvicorn main:app --port 8000     # in another terminal
    python tests/perf_load.py [base_url] [users] [seconds]
"""
import statistics
import sys
import threading
import time

import httpx
import psutil

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
USERS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
DURATION = int(sys.argv[3]) if len(sys.argv) > 3 else 20

latencies, errors = [], []
lock = threading.Lock()


def worker(stop_at: float) -> None:
    with httpx.Client(base_url=BASE, timeout=30) as c:
        # (request, status code that counts as success)
        calls = [
            (lambda: c.get("/"), 200),
            (lambda: c.get("/health"), 200),
            (lambda: c.post("/qa", json={"text": ""}), 400),
        ]
        i = 0
        while time.time() < stop_at:
            call, expected = calls[i % len(calls)]
            i += 1
            started = time.perf_counter()
            try:
                ok = call().status_code == expected
            except httpx.HTTPError:
                ok = False
            elapsed = time.perf_counter() - started
            with lock:
                latencies.append(elapsed)
                if not ok:
                    errors.append(1)


def find_server_process():
    for proc in psutil.process_iter(["cmdline"]):
        cmd = " ".join(proc.info["cmdline"] or [])
        if "uvicorn" in cmd and "main:app" in cmd:
            return proc
    return None


def main() -> None:
    proc = find_server_process()
    cpu, mem = [], []
    stop_at = time.time() + DURATION
    threads = [threading.Thread(target=worker, args=(stop_at,)) for _ in range(USERS)]
    started = time.time()
    for t in threads:
        t.start()
    while time.time() < stop_at and proc:
        cpu.append(proc.cpu_percent(interval=1.0))
        mem.append(proc.memory_info().rss / 1e6)
    for t in threads:
        t.join()
    total = time.time() - started
    lat = sorted(latencies)
    print(f"virtual users      : {USERS}")
    print(f"duration (s)       : {total:.1f}")
    print(f"requests           : {len(lat)}")
    print(f"throughput (req/s) : {len(lat) / total:.1f}")
    print(f"avg response (s)   : {statistics.mean(lat):.3f}")
    print(f"p95 response (s)   : {lat[int(len(lat) * .95) - 1]:.3f}")
    print(f"max response (s)   : {lat[-1]:.3f}")
    print(f"error rate (%)     : {len(errors) / len(lat) * 100:.2f}")
    if cpu:
        print(f"server CPU avg/max : {statistics.mean(cpu):.0f}% / {max(cpu):.0f}% (of one core)")
        print(f"server RSS avg/max : {statistics.mean(mem):.0f} MB / {max(mem):.0f} MB")


if __name__ == "__main__":
    main()
