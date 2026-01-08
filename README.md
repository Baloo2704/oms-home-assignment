```markdown
# OMS QA Automation Assignment

![Build Status](https://github.com/Baloo2704/oms-home-assignment/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## 📌 Project Overview
This repository contains a robust **Test Automation Framework** designed to validate the Order Management System (OMS) API. It focuses on **Continuous Validation**, data consistency, and integration testing using a Dockerized environment.

The solution simulates a real-world DevOps environment where tests run against a microservice architecture (FastAPI + MongoDB) automatically via CI/CD.

---

## ✅ Assignment Requirements
This project was built to satisfy the following specific deliverables:
1.  **Containerized Environment:** The API, Database, and Tests must run inside Docker.
2.  **CI/CD Integration:** Tests must trigger automatically on GitHub pushes/PRs.
3.  **Parallel Execution:** Tests must run concurrently to optimize performance (`pytest-xdist`).
4.  **Artifacts:** Test results (XML) must be saved and downloadable from the CI pipeline.
5.  **Data Consistency:** Tests must verify data directly in MongoDB, not just rely on API responses.

---

## 📋 System Requirements
Before running the project, ensure you have the following installed:

* **Docker & Docker Compose**
    * *Note: This project uses Docker Compose V2 syntax (`docker compose`). If you are on an older Linux setup using V1 (`docker-compose`), you may need to install the compose plugin.*
* **Python 3.9+** (Only if running tests locally without Docker)
* **Git** (For version control)

---

## 🚀 How to Run (Method 1: Docker)
**Recommended.** This method requires zero Python configuration and runs the exact same way as the CI pipeline.

### Step 1: Clone and Enter
```bash
git clone https://github.com/Baloo2704/oms-home-assignment.git
cd oms_home_assignment

```

### Step 2: Run the Suite

Execute the following command to spin up the App, DB, and run all tests in parallel:

```bash
docker compose up --build --exit-code-from tests

```

### Step 3: View Results

* **Success:** You will see a `0` exit code and green logs.
* **Report:** The test report is generated at `reports/results.xml` (mapped to your local folder).
* **Cleanup:** To stop the containers, run: `docker compose down`.

---

## 🛠 How to Run (Method 2: Local Development)

Use this method for debugging code, writing new tests, or when you need to see live logs in the terminal.

### Step 1: Environment Setup

Create a virtual environment and install dependencies:

```bash
# 1. Create venv
python -m venv venv

# 2. Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install Requirements
pip install -r requirements.txt

```

### Step 2: Start Infrastructure

You need MongoDB and the API running in the background. You can use Docker just for the services:

```bash
docker compose up -d mongodb oms_app

```

*(Or run `mock_api_server.py` manually if you have MongoDB installed locally)*

### Step 3: Run Tests

Run pytest from the root directory.

**Option A: Debug Mode (See Logs)**
Runs sequentially so you can see live logs in the terminal.

```bash
pytest -n0

```

**Option B: Fast Mode (Parallel)**
Runs on multiple cores (logs are hidden until the end).

```bash
pytest -n auto

```

---

## 📂 Project Structure

```text
oms_qa_assignment/
├── .github/workflows/   # CI/CD Pipeline configuration
├── mock_services/       # The System Under Test (FastAPI Server)
├── tests/               # Test Suite
│   ├── utils/           # Helper libraries (API Client, Data Models)
│   ├── conftest.py      # Fixtures (DB connection, Setup/Teardown)
│   └── test_orders_api.py   # API Integration Tests
├── docker-compose.yml   # Orchestration for DB, App, and Tests
├── Dockerfile.app       # Container definition for the API
├── pytest.ini           # Pytest configuration
└── requirements.txt     # Python dependencies

```

## 📝 Contact

**Author:** Dani Finkelstein
**Submission Date:** January 2026
