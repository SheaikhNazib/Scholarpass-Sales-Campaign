from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.config import get_settings
import logging

settings = get_settings()
# Support both argon2 and bcrypt so the app can verify passwords created by either
# (some environments may not have argon2 available). Passlib will pick the
# correct scheme based on the stored hash's prefix when verifying.
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

log = logging.getLogger(__name__)

security_scheme = HTTPBearer()

class SecurityService:
    @staticmethod
    def hash_password(password: str) -> str:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            # Log and re-raise so callers can handle errors if hashing truly fails
            log.exception("Password hashing failed")
            raise

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # If verification fails due to missing scheme or other issues,
            # return False (authentication will fail) but don't crash the app.
            log.exception("Password verification error")
            return False

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
):
    from src.modules.user.models import AppUser
    try:
        payload = SecurityService.decode_token(auth.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    user = db.query(AppUser).filter(AppUser.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_super_admin(
    current_user = Depends(get_current_user)
):
    if current_user.primary_role_name != "Super Admin" and current_user.username != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions to perform this action"
        )
    return current_user
