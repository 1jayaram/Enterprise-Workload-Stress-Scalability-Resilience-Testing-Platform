# Enterprise Workload Stress, Scalability & Resilience Testing Platform

A Python workload-scheduler simulator plus an automated QA platform. It demonstrates priority queues, resource-aware dispatch, worker slots, REST/CLI interfaces, persistence, load generation, process monitoring, fault simulation, and performance regression checks.

**Scope:** a local multi-worker simulator. Workers execute in threads within one API process; this is not a production distributed scheduler. The project is designed to demonstrate QA engineering fundamentals and provide a base for process-level worker orchestration.

## Stack
Python 3.12, FastAPI, SQLite/WAL, Pytest, HTTPX, Locust, psutil, Matplotlib, Docker, GitHub Actions.

## Phase 1 — Environment

In VS Code terminal (PowerShell):

```powershell
conda create -n workload-qa python=3.12 -y
conda activate workload-qa
python -m pip install --upgrade pip
pip install -r requirements.txt
New-Item -ItemType Directory -Force data,reports
```

## Phase 2 — Start the scheduler

```powershell
uvicorn workload_platform.api:app --reload
```

Swagger API documentation: http://127.0.0.1:8000/docs

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

## Phase 3 — Submit and inspect jobs

Open a second terminal:

```powershell
python -m workload_platform.cli submit demo-job --duration 2 --cpu 1 --memory 256 --priority 5
python -m workload_platform.cli jobs
python -m workload_platform.cli cluster
```

The API also supports `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`, `DELETE /jobs/{id}`, and `GET /cluster`.

## Phase 4 — Automated tests

```powershell
pytest -v
pytest --cov=workload_platform --cov-report=term-missing
```

Tests cover API health, submission, invalid payloads, resource admission, missing jobs, filters, cluster status, and restart recovery.

## Phase 5 — Concurrent load experiment

Keep the API running:

```powershell
python -m qa_platform.runner --jobs 100 --concurrency 10 --duration 0.05
```

Output: `reports/latest.json`. The report includes measured request latency (mean/p50/p95/p99), completed-job throughput, submission errors and process CPU/memory samples. Values are measured on your machine; no performance results are hardcoded.

## Phase 6 — Visualize performance

```powershell
python -m qa_platform.plot_report reports/latest.json
```

Graph: `reports/latency.png`.

## Phase 7 — Spike test

```powershell
python scripts/spike_test.py
```

This submits a normal batch, then a 10x burst. Observe queue drain time and terminal states.

## Phase 8 — Endurance test

First validate for two minutes:

```powershell
python scripts/endurance_test.py --minutes 2 --batch 30
```

Then perform the full one-hour run:

```powershell
python scripts/endurance_test.py --minutes 60 --batch 100
```

Monitor memory and failures throughout.

## Phase 9 — Fault injection

```powershell
python scripts/fault_injection.py
```

This injects task-level failures using a probability field. It is not equivalent to killing a worker operating-system process; process-kill testing is a further extension.

## Phase 10 — Locust load test

```powershell
locust -f locustfile.py --host http://127.0.0.1:8000
```

Open the local URL printed by Locust. Start with 10 users, then increase gradually (e.g. 25, 50, 100). Record request rate, failures, median and p95 response time.

## Phase 11 — Performance regression

Save the baseline:

```powershell
Copy-Item reports/latest.json reports/baseline.json
```

Run the exact same workload after a code change, then compare:

```powershell
python -m qa_platform.regression reports/baseline.json reports/latest.json
```

The default rule flags more than 15% degradation in mean, p95 or p99 API submission latency.

## Phase 12 — Docker and CI

```powershell
docker compose up --build
```

Visit http://localhost:8000/docs. GitHub Actions runs the Pytest suite on pushes and pull requests.

## Experiment plan

| Test | Workload | Measurements |
|---|---|---|
| Baseline | 100 jobs, 10 clients | Mean/p95/p99, throughput |
| Load | 100 / 500 / 1,000 jobs | Latency, errors |
| Scalability | 1 / 2 / 4 / 8 workers | Throughput, scaling efficiency |
| Stress | Increase Locust users | First sustained error/timeout |
| Spike | 20 then 200 jobs | Queue drain and recovery |
| Endurance | 60 minutes | Memory trend, error trend |
| Fault | 25% task failure probability | Completed/failed counts |
| Regression | Same workload, two builds | Percent deviation |

## Limitations and next engineering upgrades

- Worker execution currently uses a thread pool in one process. True worker-process kill/restart requires a separate worker executable, heartbeats and leases.
- Restart recovery requeues jobs marked running; this is at-least-once behavior, not exactly-once execution. Production designs need idempotency keys and durable execution attempts.
- SQLite is suitable for a local simulator. Multi-instance deployments should use PostgreSQL or another server database.
- Resource reservations use requested CPU/RAM values; they do not enforce OS-level resource limits.
- Add race-condition tests, fairness tests, repeated restart tests, worker heartbeat expiry, API timeout/network interruption, and process-level fault injection before describing this as production-grade resilience.

## Resume description

**Enterprise Workload Stress, Scalability & Resilience Testing Platform | Python, FastAPI, Pytest, SQLite, Locust, psutil, Docker**
- Developed a resource-aware workload scheduler featuring priority-based queuing, worker allocation, job lifecycle management and persistent state.
- Built automated API and recovery tests covering invalid inputs, resource constraints, cancellation, persistence and restart behavior.
- Implemented concurrent workload generation and monitoring to measure latency, throughput, CPU and memory consumption.
- Created repeatable spike, endurance and task-failure experiments with JSON reporting and automated performance-regression thresholds.

Add numeric achievements to your resume only after running the experiments and recording the results.
