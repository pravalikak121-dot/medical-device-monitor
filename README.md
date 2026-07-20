# Healthcare Device Monitoring Application

A professional healthcare device monitoring application built with Python, FastAPI, Streamlit, and PostgreSQL. This application demonstrates enterprise-level features including authentication, role-based access control, AI-powered alerts, PDF reports, and cloud deployment capabilities.

> **Production-Ready Application**: This is a comprehensive demo application designed for portfolio use. It showcases full-stack development, DevOps, and cloud deployment best practices.

## Features

### Core Functionality
- **Real-time Device Monitoring**: Monitor healthcare device status, battery levels, and signal strength
- **Alert Management**: Create, track, and resolve device alerts with severity levels
- **Device Health Reports**: Generate PDF reports of device health data
- **Dashboard**: Beautiful, responsive web dashboard for data visualization

### Authentication & Security
- **User Registration & Login**: Secure JWT-based authentication
- **Role-Based Access Control (RBAC)**: Admin, Doctor, Nurse, and Technician roles
- **Password Hashing**: Bcrypt password hashing for security
- **Token Management**: Automatic token expiration and refresh

### Advanced Features
- **AI Alert Summaries**: Automatic alert summarization using OpenAI API (with fallback rule-based system)
- **Email Alerts**: Send critical alerts via email notifications
- **PDF Report Generation**: Professional PDF reports with charts and data
- **SQLite/PostgreSQL Database**: Persistent data storage with SQLAlchemy ORM

### Deployment Options
- **Docker Containerization**: Full Docker and Docker Compose support
- **AWS Deployment**: CloudFormation templates for EC2, ECS, and RDS
- **Heroku Deployment**: Procfile and buildpacks configured
- **Azure Deployment**: App Service and Web App ready
- **Google Cloud Ready**: Cloud Run and Cloud SQL compatible

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PyJWT** - JWT authentication
- **Passlib** - Password hashing
- **ReportLab** - PDF generation
- **OpenAI** - AI-powered alert summaries
- **python-jose** - OAuth2 security

### Frontend
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation
- **Matplotlib** - Data visualization

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production database

### Deployment & DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Gunicorn** - WSGI application server
- **AWS** - Cloud infrastructure
- **Heroku** - Platform-as-a-Service

## Project Structure

```
medical-device-monitor/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with all endpoints
│   ├── models.py            # SQLAlchemy ORM models
│   ├── auth.py              # Authentication and JWT tokens
│   ├── database_connection.py  # Database configuration
│   ├── database.py          # Legacy in-memory database (deprecated)
│   ├── simulator.py         # Device simulation logic
│   ├── pdf_service.py       # PDF report generation
│   ├── email_service.py     # Email alert functionality
│   └── ai_service.py        # AI alert summarization
├── dashboard/
│   ├── __init__.py
│   └── dashboard.py         # Streamlit dashboard
├── deploy/
│   └── aws-cloudformation.json  # AWS deployment template
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container orchestration
├── Procfile                 # Heroku deployment configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── DEPLOYMENT.md            # Cloud deployment guide
└── README.md                # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/medical-device-monitor.git
cd medical-device-monitor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**

Terminal 1 - Start API:
```bash
uvicorn app.main:app --reload
```

Terminal 2 - Start Dashboard:
```bash
streamlit run dashboard/dashboard.py
```

6. **Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services
# API: http://localhost:8000
# Dashboard: http://localhost:8501
# Database: localhost:5432
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token

### Devices
- `GET /api/v1/devices` - Get all devices (filtered by role)
- `GET /api/v1/devices/{device_id}` - Get specific device
- `POST /api/v1/devices` - Create new device (Admin only)

### Alerts
- `GET /api/v1/alerts` - Get all alerts (filtered by role)
- `POST /api/v1/alerts` - Create new alert (Doctor/Admin)

### Reports
- `GET /api/v1/reports/devices/pdf` - Generate device report PDF
- `GET /api/v1/reports/alerts/summary` - Get AI alert summary

### Health
- `GET /health` - Health check
- `GET /` - API info

## User Roles

| Role | Permissions |
|------|-----------|
| **Admin** | Full access to all features, device management, user management |
| **Doctor** | View/create alerts, generate reports for assigned devices |
| **Nurse** | View assigned devices, create alerts |
| **Technician** | View assigned devices, view alerts |

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./medical_device_monitor.db

# Security
SECRET_KEY=your-secret-key-min-32-characters

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# OpenAI API (for AI alert summaries)
OPENAI_API_KEY=sk-...

# Application
DEBUG=True
```

## Features Explained

### Authentication
- Secure JWT-based authentication with 30-minute token expiration
- Bcrypt password hashing
- Role-based access control on all endpoints

### Database
- SQLAlchemy ORM with PostgreSQL support
- Automatic schema creation on startup
- Relationship management for users, devices, alerts, and reports

### AI Integration
- OpenAI GPT-3.5 for intelligent alert summarization
- Fallback rule-based summaries if API is unavailable
- Caching support for frequently accessed summaries

### Email Alerts
- HTML-formatted alert emails
- Severity-based color coding
- Configurable SMTP server

### PDF Reports
- Professional report generation with ReportLab
- Device health tables with status highlighting
- Alert summary reports with critical counts

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_api.py::test_health_check
```

## Deployment

### Cloud Platforms Supported
- **AWS** (EC2, ECS, RDS)
- **Heroku** (Platform as a Service)
- **Azure** (App Service, PostgreSQL)
- **Google Cloud** (Cloud Run, Cloud SQL)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for each platform.

## Best Practices Implemented

- ✅ Modular code structure
- ✅ Comprehensive error handling
- ✅ Security best practices (JWT, hashing, RBAC)
- ✅ Database abstraction with ORM
- ✅ API documentation (Swagger/OpenAPI)
- ✅ Docker containerization
- ✅ Environment configuration
- ✅ Type hints throughout codebase
- ✅ Logging and monitoring
- ✅ Health checks

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@example.com or open an issue on GitHub.

## Roadmap

- [ ] Real-time WebSocket updates
- [ ] Advanced analytics dashboard
- [ ] Machine learning for predictive maintenance
- [ ] Mobile app (iOS/Android)
- [ ] Third-party integrations (Slack, Microsoft Teams)
- [ ] Multi-tenancy support
- [ ] Audit logging
- [ ] Advanced reporting with filters
- [ ] API rate limiting
- [ ] CDN integration

## Author

Created as a portfolio project to demonstrate full-stack development, cloud deployment, and DevOps practices.

---

**Note**: This is a demonstration application. For production use with real medical devices, additional compliance, security, and regulatory considerations are required.

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
