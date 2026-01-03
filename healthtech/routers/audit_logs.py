from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from healthtech import models, schemas
from healthtech.database import SessionLocal
from typing import List
from healthtech.dependencies import require_role


router = APIRouter(prefix="/audit_logs", tags=["Audit Logs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_model=List[schemas.AuditLogResponse])
def get_audit_log(db: Session = Depends(get_db)):
    return db.query(models.AuditLog).all()