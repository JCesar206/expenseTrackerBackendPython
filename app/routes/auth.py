import logging
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserLogin, UserRegister, UserResponse, TokenResponse
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer(auto_error=False)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    email = str(data.email).strip().lower()
    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese email.",
        )

    user = User(
        email=email,
        password_hash=hash_password(data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese email.",
        )

    logger.info("Usuario registrado: id=%s", user.id)
    return user

@router.post("/login", response_model=TokenResponse)
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    email = str(data.email).strip().lower()
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if (
        user is None
        or not verify_password(data.password, user.password_hash)
        or not user.is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)
    logger.info("Inicio de sesión correcto: id=%s", user.id)
    return TokenResponse(access_token=token)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token ausente, inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise unauthorized
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized

    return user

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
