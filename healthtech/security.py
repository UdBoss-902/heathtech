from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

#Secret & algorithm (replace with env vars in production)
JWT_SECRET = "CHANGE_ME_TO_ENV_SECRET"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def create_access_token(subject: str, role: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithm=[JWT_ALGORITHM])
    except JWTError:
        return None