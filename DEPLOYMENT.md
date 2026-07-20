# Deployment Guide - Medical Device Monitor

## Overview
This guide covers deploying the Medical Device Monitor application to various cloud platforms.

## Prerequisites
- Docker installed
- Git installed
- Cloud platform CLI tools (AWS CLI, Azure CLI, etc.)
- Environment variables configured

## Local Development

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### Running Locally
```bash
# Terminal 1: Start API
uvicorn app.main:app --reload

# Terminal 2: Start Dashboard
streamlit run dashboard/dashboard.py
```

Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Docker Deployment

### Build Docker Image
```bash
docker build -t medical-device-monitor:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

Services:
- API: http://localhost:8000
- Dashboard: http://localhost:8501
- Database: postgres:5432

## Cloud Deployment

### AWS Deployment

#### Option 1: EC2 + RDS
```bash
# 1. Create CloudFormation stack
aws cloudformation create-stack \
  --stack-name medical-monitor \
  --template-body file://deploy/aws-cloudformation.json \
  --parameters ParameterKey=EnvironmentName,ParameterValue=production

# 2. SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Clone repository
git clone your-repo-url
cd medical-device-monitor

# 4. Setup and run
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Option 2: ECS + Fargate
```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name medical-device-monitor

# 2. Build and push image
docker build -t medical-device-monitor:latest .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag medical-device-monitor:latest your-account.dkr.ecr.us-east-1.amazonaws.com/medical-device-monitor:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/medical-device-monitor:latest

# 3. Create ECS task definition and service
# Use AWS Console or CLI to create task definition
```

### Heroku Deployment

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create medical-device-monitor

# 3. Add buildpacks
heroku buildpacks:add heroku/python

# 4. Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-api-key
heroku config:set DATABASE_URL=postgres://...

# 5. Deploy
git push heroku main

# 6. Run migrations
heroku run python -c "from app.database_connection import init_db; init_db()"

# 7. Open app
heroku open
```

### Azure Deployment

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name medical-monitor-rg --location eastus

# 3. Create App Service Plan
az appservice plan create \
  --name medical-monitor-plan \
  --resource-group medical-monitor-rg \
  --sku B1 \
  --is-linux

# 4. Create Web App
az webapp create \
  --resource-group medical-monitor-rg \
  --plan medical-monitor-plan \
  --name medical-device-monitor \
  --runtime "PYTHON|3.11"

# 5. Configure deployment
git remote add azure your-azure-git-url
git push azure main

# 6. Set app settings
az webapp config appsettings set \
  --name medical-device-monitor \
  --resource-group medical-monitor-rg \
  --settings SECRET_KEY=your-secret-key
```

### Google Cloud Deployment

```bash
# 1. Set project
gcloud config set project your-project-id

# 2. Build image with Cloud Build
gcloud builds submit --tag gcr.io/your-project/medical-monitor

# 3. Deploy to Cloud Run
gcloud run deploy medical-monitor \
  --image gcr.io/your-project/medical-monitor \
  --platform managed \
  --region us-central1 \
  --set-env-vars SECRET_KEY=your-secret-key

# 4. Create Cloud SQL instance
gcloud sql instances create medical-monitor-db \
  --database-version POSTGRES_15 \
  --region us-central1
```

## Environment Variables

Required environment variables:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-random-secret-key-min-32-chars
OPENAI_API_KEY=sk-...
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

## Database Migration

### Initial Setup
```bash
python -c "from app.database_connection import init_db; init_db()"
```

### Create Default Admin User
```bash
python -c "
from sqlalchemy.orm import Session
from app.database_connection import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

db = SessionLocal()
admin = User(
    username='admin',
    email='admin@example.com',
    hashed_password=get_password_hash('admin123'),
    role=UserRole.ADMIN
)
db.add(admin)
db.commit()
print('Admin user created!')
"
```

## Monitoring & Logging

### Health Checks
```bash
curl http://your-app/health
```

### API Documentation
- Swagger UI: `http://your-app/docs`
- ReDoc: `http://your-app/redoc`

### Logs
```bash
# Heroku
heroku logs --tail

# AWS CloudWatch
aws logs tail /aws/lambda/your-function --follow

# Google Cloud Logging
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json
```

## Security Considerations

1. **Change default credentials**: Update SECRET_KEY and database passwords
2. **Use HTTPS**: Enable SSL/TLS certificates
3. **Database**: Use managed database services (RDS, Cloud SQL)
4. **Secrets**: Use cloud provider secret management
5. **API Keys**: Rotate OpenAI and email credentials regularly
6. **CORS**: Configure CORS for your frontend domain
7. **Rate Limiting**: Implement rate limiting for production

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
psql postgresql://user:password@host:5432/dbname
```

### API Not Starting
```bash
# Check logs
docker logs container-id

# Test locally
uvicorn app.main:app --reload --log-level debug
```

### Dashboard Connection Issues
```bash
# Check API is accessible
curl http://api-host/health

# Update API_URL in dashboard configuration
```

## Support
For issues or questions, refer to the README.md or documentation.
