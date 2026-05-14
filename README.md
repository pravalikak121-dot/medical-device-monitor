# Healthcare Device Monitoring App

A simulated healthcare device monitoring application built with Python, FastAPI, Streamlit, Pytest, and GitHub Actions.

This project is designed as a portfolio project for Python Automation Engineer, SDET, QA Automation Engineer, DevOps Automation Engineer, and Python Backend Engineer roles.

> Note: This is a simulated demo application. It does not connect to real medical devices or real patient data.

## Project Overview

The application simulates healthcare device telemetry and displays device health information in a dashboard.

It monitors:

- Device online/offline status
- Battery level
- Signal strength
- Device alerts
- Device health reports

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pytest
- Pandas
- Matplotlib
- Docker
- GitHub Actions

## Features

- REST API backend using FastAPI
- Streamlit dashboard frontend
- Simulated healthcare device telemetry
- Battery and signal monitoring
- Alert generation for low battery, weak signal, and offline devices
- CSV report download
- Unit/API testing with Pytest
- CI/CD workflow using GitHub Actions
- Docker support

## Project Structure

```text
medical-device-monitor/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── simulator.py
├── dashboard/
│   ├── __init__.py
│   └── dashboard.py
├── reports/
│   ├── __init__.py
│   └── report_generator.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/devices` | Get all devices |
| GET | `/devices/{device_id}` | Get device by ID |
| POST | `/devices` | Create a device |
| PUT | `/devices/{device_id}/status` | Update device status |
| GET | `/alerts` | Get all active alerts |
| POST | `/devices/simulate` | Refresh simulated telemetry |

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/medical-device-monitor.git
cd medical-device-monitor
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run FastAPI backend

```bash
uvicorn app.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Run Streamlit dashboard

Open a second terminal:

```bash
streamlit run dashboard/dashboard.py
```

## How to Run Tests

```bash
pytest -v
```

Expected result:

```text
9 passed
```

## Docker Commands

Build Docker image:

```bash
docker build -t medical-device-monitor .
```

Run Docker container:

```bash
docker run -p 8000:8000 medical-device-monitor
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Resume Bullet

Built a simulated healthcare device monitoring application using Python, FastAPI, Streamlit, and Pytest to track device status, battery level, signal strength, alert generation, dashboard visualization, CSV reporting, Docker support, and CI/CD validation through GitHub Actions.

## Future Enhancements

- Add SQLite database persistence
- Add user login/authentication
- Add role-based dashboard views
- Add PDF report generation
- Add email alerts
- Add AI-generated alert summaries
- Deploy to cloud platform
