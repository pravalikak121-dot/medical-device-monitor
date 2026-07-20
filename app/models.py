from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    TECHNICIAN = "technician"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.NURSE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    devices = relationship("Device", back_populates="assigned_to_user")
    alerts = relationship("Alert", back_populates="created_by_user")


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String, unique=True, index=True)
    patient_id = Column(String, index=True)
    device_type = Column(String)
    status = Column(String)
    battery_level = Column(Integer)
    signal_strength = Column(Integer)
    last_sync = Column(DateTime, default=datetime.utcnow)
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assigned_to_user = relationship("User", back_populates="devices")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    alert_type = Column(String)
    severity = Column(String)  # Low, Medium, High, Critical
    message = Column(String)
    ai_summary = Column(String, nullable=True)
    is_resolved = Column(Boolean, default=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    device = relationship("Device", back_populates="alerts")
    created_by_user = relationship("User", back_populates="alerts")


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    report_type = Column(String)  # daily, weekly, monthly, custom
    generated_by_user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailAlert(Base):
    __tablename__ = "email_alerts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    sent_to = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # sent, failed, pending
