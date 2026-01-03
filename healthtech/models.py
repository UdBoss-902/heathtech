from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from healthtech.database import Base
import enum
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    dob = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=True)

    user = relationship("User", backref="patient_profile")


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    user = relationship("User", backref="doctor_profile")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String, default="booked")
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")
    doctor = relationship("Doctor")

    
class UserRole(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"
    id =  Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="audit_logs")