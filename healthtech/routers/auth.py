from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from healthtech import models, schemas
from healthtech.database import SessionLocal
from healthtech.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, details = "Email already registerd")
    
    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=models.UserRole(payload.role.value)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

class TokenResponse(schemas.BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm provides: username, password
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token)

