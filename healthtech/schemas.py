from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class PatientBase(BaseModel):
    name: str
    email: str
    dob: str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity: str
    entity_id: int
    user_id: int | None
    timestamp: datetime

    class Config:
        from_attributes = True
    
class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True