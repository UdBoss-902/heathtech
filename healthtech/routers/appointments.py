from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from healthtech import models, schemas
from healthtech.database import SessionLocal
from healthtech.dependencies import require_role, get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/my", response_model=list[schemas.AppointmentResponse], dependencies=[Depends(require_role("patient"))])
def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    patient = db.query(models.Patient).filter(models.Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient.id).app()



@router.get("/mine", response_model=list[schemas.AppointmentResponse], dependencies=[Depends(require_role("doctor"))])
def get_assigned_appointment(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id).all()


@router.get("/", response_model=list[schemas.AppointmentResponse], dependencies=[Depends(require_role("admin"))])
def list_all_appointments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    return db.query(models.Appointment).offset(skip).limit(limit).all()



@router.post("/", response_model=schemas.AppointmentResponse, dependencies=[Depends(require_role("admin", "doctor"))])
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # Check patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_appointment = models.Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        scheduled_time=appointment.scheduled_time,
        status="booked"
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
