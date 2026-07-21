from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Optional

from app.database_connection import get_db, init_db
from app.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    decode_access_token
)
from app.models import User, Device, Alert, UserRole
from app.pdf_service import generate_device_report_pdf
from app.ai_service import generate_alert_summary, generate_batch_summary
from app.simulator import calculate_status

# Initialize database on startup
init_db()

app = FastAPI(
    title="Healthcare Device Monitoring API",
    description="Professional healthcare device monitoring with authentication and reporting.",
    version="2.0.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.NURSE


class UserLogin(BaseModel):
    username: str
    password: str


class DeviceCreate(BaseModel):
    device_id: str = Field(..., example="DEV-2001")
    patient_id: str = Field(..., example="PAT-501")
    device_type: str = Field(default="Sleep Therapy Monitor")
    battery_level: int = Field(..., ge=0, le=100, example=87)
    signal_strength: int = Field(..., ge=0, le=100, example=92)
    assigned_to_user_id: Optional[int] = None


class AlertCreate(BaseModel):
    device_id: int
    alert_type: str
    severity: str
    message: str


class StatusUpdate(BaseModel):
    status: str = Field(..., example="Online")


# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get the current authenticated user from token"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_doctor_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require doctor or admin role"""
    if current_user.role not in [UserRole.DOCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor or Admin access required"
        )
    return current_user


# Authentication endpoints
@app.post("/api/v1/auth/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}


@app.post("/api/v1/auth/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and get access token"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/v1/users")
def get_users(role: Optional[UserRole] = None, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get users, optionally filtering by role (admin only)"""
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    users = query.order_by(User.username).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role.value
        }
        for u in users
    ]


@app.get("/api/v1/users/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Return current authenticated user info"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value
    }


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Device endpoints with role-based access
@app.get("/api/v1/devices")
def get_devices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all devices (filtered by user role)"""
    if current_user.role == UserRole.ADMIN:
        devices = db.query(Device).all()
    else:
        devices = db.query(Device).filter(Device.assigned_to_user_id == current_user.id).all()
    
        {
            "id": d.id,
            "device_id": d.device_id,
            "patient_id": d.patient_id,
            "device_type": d.device_type,
            "status": d.status,
            "battery_level": d.battery_level,
            "signal_strength": d.signal_strength,
            "last_sync": d.last_sync,
            "assigned_to_user_id": d.assigned_to_user_id,
            "assigned_to_username": d.assigned_to_user.username if d.assigned_to_user else None
        }
        for d in devices:

@app.post("/api/v1/devices", status_code=201)
def create_device(
    device: DeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new device"""
    existing = db.query(Device).filter(Device.device_id == device.device_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Device already exists")
    
    assigned_to_user_id = current_user.id
    if current_user.role == UserRole.ADMIN and device.assigned_to_user_id is not None:
        assigned_to_user_id = device.assigned_to_user_id
    
    status_value = calculate_status(device.battery_level, device.signal_strength)
    new_device = Device(
        device_id=device.device_id,
        patient_id=device.patient_id,
        device_type=device.device_type,
        battery_level=device.battery_level,
        signal_strength=device.signal_strength,
        status=status_value,
        assigned_to_user_id=assigned_to_user_id
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    
    return {"message": "Device created successfully", "device_id": new_device.device_id}


@app.get("/api/v1/devices/{device_id}")
def get_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device by ID"""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if current_user.role != UserRole.ADMIN and device.assigned_to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "id": device.id,
        "device_id": device.device_id,
        "patient_id": device.patient_id,
        "device_type": device.device_type,
        "status": device.status,
        "battery_level": device.battery_level,
        "signal_strength": device.signal_strength,
        "last_sync": device.last_sync,
        "assigned_to_user_id": device.assigned_to_user_id,
        "assigned_to_username": device.assigned_to_user.username if device.assigned_to_user else None
    }


# Alert endpoints
@app.get("/api/v1/alerts")
def get_alerts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get alerts"""
    if current_user.role == UserRole.ADMIN:
        alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    else:
        alerts = db.query(Alert).join(Device).filter(
            Device.assigned_to_user_id == current_user.id,
            Alert.is_resolved == False
        ).all()
    
    return [
        {
            "id": a.id,
            "device_id": a.device.device_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "message": a.message,
            "ai_summary": a.ai_summary,
            "created_at": a.created_at
        }
        for a in alerts
    ]


@app.post("/api/v1/alerts", status_code=201)
def create_alert(
    alert: AlertCreate,
    current_user: User = Depends(require_doctor_or_admin),
    db: Session = Depends(get_db)
):
    """Create an alert"""
    device = db.query(Device).filter(Device.id == alert.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    ai_summary = generate_alert_summary({
        "device_id": device.device_id,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "message": alert.message
    })
    
    new_alert = Alert(
        device_id=alert.device_id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        message=alert.message,
        ai_summary=ai_summary,
        created_by_user_id=current_user.id
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return {
        "message": "Alert created successfully",
        "alert_id": new_alert.id,
        "ai_summary": ai_summary
    }


# Reporting endpoints
@app.get("/api/v1/reports/devices/pdf")
def get_device_report_pdf(current_user: User = Depends(require_doctor_or_admin), db: Session = Depends(get_db)):
    """Generate device health report in PDF"""
    try:
        if current_user.role == UserRole.ADMIN:
            devices = db.query(Device).all()
        else:
            devices = db.query(Device).filter(Device.assigned_to_user_id == current_user.id).all()
        
        device_dicts = [
            {
                "device_id": d.device_id,
                "patient_id": d.patient_id,
                "device_type": d.device_type,
                "status": d.status,
                "battery_level": d.battery_level,
                "signal_strength": d.signal_strength,
                "last_sync": d.last_sync.isoformat() if d.last_sync else ""
            }
            for d in devices
        ]
        
        pdf_bytes = generate_device_report_pdf(device_dicts)
        
        import base64
        return {
            "pdf": base64.b64encode(pdf_bytes).decode('utf-8'),
            "content_type": "application/pdf",
            "filename": "device_health_report.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.get("/api/v1/reports/alerts/summary")
def get_alerts_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get AI-generated alert summary"""
    if current_user.role == UserRole.ADMIN:
        alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    else:
        alerts = db.query(Alert).join(Device).filter(
            Device.assigned_to_user_id == current_user.id,
            Alert.is_resolved == False
        ).all()
    
    alert_dicts = [
        {
            "device_id": a.device.device_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "message": a.message,
            "battery_level": a.device.battery_level if a.device else 0,
            "signal_strength": a.device.signal_strength if a.device else 0
        }
        for a in alerts
    ]
    
    return generate_batch_summary(alert_dicts)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Healthcare Device Monitoring API v2.0",
        "docs": "/docs",
        "health": "/health",
        "auth": "/api/v1/auth/login"
    }
