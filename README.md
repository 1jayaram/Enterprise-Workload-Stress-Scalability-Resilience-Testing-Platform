<img width="1908" height="1031" alt="Screenshot 2026-11-06 165719" src="https://github.com/user-attachments/assets/eb785f6f-eed5-4f07-93a4-900eb5fb79fc" />
<img width="1915" height="1042" alt="Screenshot 2026-11-06 165755" src="https://github.com/user-attachments/assets/c9b9f41c-d584-4d12-8464-54366366b7ab" />
# Enterprise Workload Stress, Scalability & Resilience Testing Platform

A Python-based workload management and quality assurance platform designed to evaluate API reliability, concurrent job processing, workload scheduling, system performance and application behaviour under varying workloads.

## Project Overview

The **Enterprise Workload Stress, Scalability & Resilience Testing Platform** is a software testing project that combines backend development, automated testing and performance engineering.

The platform provides REST APIs for submitting and monitoring workloads, manages job execution through a worker-based scheduler, and uses automated testing tools to evaluate application behaviour.

The objective is to move beyond basic functional testing and explore how an application performs under concurrent requests and sustained workloads.

## Key Features

- **REST API Development:** FastAPI endpoints for workload submission, cluster monitoring and job management.
- **Workload Scheduling:** Worker-based execution and resource-capacity management.
- **Job Lifecycle Management:** Submission, execution, monitoring and cancellation of workloads.
- **Database Integration:** SQLite-based persistence for workload information and job states.
- **Automated Testing:** Pytest-based API and recovery test cases.
- **Load Testing:** Locust-based simulation of concurrent users and API requests.
- **Performance Monitoring:** Response-time, throughput and failure-rate analysis.
- **Resource Monitoring:** Process monitoring and performance metrics using psutil.
- **Stress and Endurance Testing:** Scripts for evaluating application behaviour under different workload patterns.
- **Containerisation:** Docker and Docker Compose configuration.
- **Continuous Integration:** GitHub Actions workflow for automated test execution.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| Testing Framework | Pytest |
| Performance Testing | Locust |
| Monitoring | psutil |
| API Communication | REST / HTTP |
| Containerisation | Docker |
| CI/CD | GitHub Actions |

## System Architecture

The platform consists of three main components:

### 1. Workload Management Backend

The backend handles incoming API requests, job submission, workload scheduling, worker execution and database operations.

### 2. Quality Assurance and Monitoring

The QA component generates workloads, collects execution information, monitors performance and produces test results.

### 3. Performance Testing

Locust simulates concurrent users interacting with the backend APIs. Performance metrics are collected to evaluate throughput, response times and request failures.

```text
              Locust Load Generator
                       |
                       v
                FastAPI Backend
                       |
              Workload Scheduler
                       |
                Worker Pool
                       |
                 SQLite DB
                       |
                       v
             QA & Monitoring Layer
                       |
             Performance Reports
```

## Project Structure

```text
enterprise-workload-qa-platform/
│
├── workload_platform/       # Backend application
├── qa_platform/             # QA and monitoring modules
├── tests/                   # Automated test cases
├── scripts/                 # Stress and endurance tests
├── .github/workflows/       # CI configuration
│
├── locustfile.py            # Locust workload definition
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later (use a version compatible with the dependencies)
- pip
- Git
- VS Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/enterprise-workload-qa-platform.git
cd enterprise-workload-qa-platform
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI backend:

```bash
python -m uvicorn workload_platform.api:app --host 127.0.0.1 --port 8000 --reload
```

The backend will be available at:

- Health: http://127.0.0.1:8000/health
- Cluster information: http://127.0.0.1:8000/cluster
- Job management: http://127.0.0.1:8000/jobs
- API documentation: http://127.0.0.1:8000/docs

Keep the backend terminal running while executing tests.

## Automated Testing

Run the Pytest test suite:

```bash
python -m pytest tests/ -v
```

Generate an HTML test report if the pytest-html dependency is installed:

```bash
python -m pytest tests/ -v --html=reports/test-report.html --self-contained-html
```

## Performance and Load Testing

Start Locust:

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

Open the Locust interface:

http://localhost:8089

Configure the number of users and spawn rate, then start the test.

### Spike Testing

```bash
python -m scripts.spike_test
```

### Endurance Testing

```bash
python -m scripts.endurance_test --minutes 2 --batch 30
```

### Fault Injection

```bash
python -m scripts.fault_injection
```

Use the actual command-line arguments supported by each script if they differ from these examples.

## Performance Testing Results

An initial Locust test was conducted against the local FastAPI application with 10 concurrent users.

### Observed Results

| Metric | Result |
|---|---:|
| Concurrent Users | 10 |
| Total Requests | 5,922 |
| Requests Per Second | 27.1 |
| Failure Rate | 0% |
| Average Response Time | 46.83 ms |
| Median Response Time | 40 ms |
| 95th Percentile | 100 ms |
| 99th Percentile | 170 ms |

### Endpoint-Level Results

| Endpoint | Requests | Failures | Average Response |
|---|---:|---:|---:|
| GET /cluster | 884 | 0 | 22.94 ms |
| POST /jobs | 4,036 | 0 | 55.18 ms |
| GET /jobs?limit=100 | 1,002 | 0 | 34.26 ms |

**Observation:** During this particular test run, all 5,922 recorded requests completed without reported failures. The aggregated average response time was 46.83 ms.

These figures represent one local test run and should not be interpreted as production capacity or a validated scalability limit. Results can vary with hardware, database state, workload configuration and test duration.

## Engineering Concepts Explored

- Functional API testing
- Concurrent request handling
- Workload scheduling
- Resource-capacity management
- Job lifecycle validation
- Performance benchmarking
- Response-time percentile analysis
- Failure-rate monitoring
- Recovery and reliability testing
- Continuous integration

## Future Improvements

- Increase concurrency and evaluate system behaviour at 25, 50 and 100 users.
- Implement deeper CPU and memory monitoring of the backend process.
- Introduce process-level worker isolation.
- Add heartbeat monitoring and automatic worker recovery.
- Implement retry mechanisms and idempotent job submission.
- Expand fault injection to simulate worker and network failures.
- Add automated performance regression comparisons.
- Develop a dedicated web dashboard for real-time monitoring.

## Project Scope and Limitations

The current implementation uses a local FastAPI application, SQLite persistence and an in-process worker scheduler. It is intended as an engineering and QA testing platform, not a production-grade distributed orchestration system.

The reported performance results are specific to the local development environment.

## Author

**Jayaram S**

Software Quality Assurance | Python | API Testing | Performance Engineering | Automation Testing

## License

This project is available under the MIT License. Add a `LICENSE` file to the repository if you intend to distribute it under that license.
