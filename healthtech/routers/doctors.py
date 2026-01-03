from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from healthtech import models, schemas
from healthtech.database import SessionLocal

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = models.Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
