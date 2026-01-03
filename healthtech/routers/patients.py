from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from healthtech import models, schemas
from healthtech.database import SessionLocal
from healthtech.dependencies import get_current_user
from healthtech.utils.audit import log_action

router = APIRouter(prefix="/patients", tags=["Patients"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_patient = models.Patient(name=patient.name, email=patient.email, dob=patient.dob)
    db.add(db_patient)
    db.commit()
    db.refresh(db.patient)

    log_action(db, current_user.id, "CREATE_PATIENT", db_patient.id)



    return db_patient
    

@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

