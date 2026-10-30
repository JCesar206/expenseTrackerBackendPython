from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    return password_hasher.verify(
        plain_password,
        password_hash,
    )

def create_access_token(user_id: int) -> str:
    if (
        not settings.jwt_secret_key
        or settings.jwt_secret_key
        == "REPLACE_WITH_A_RANDOM_SECRET"
        or settings.jwt_secret_key
        == "GENERATE_A_RANDOM_SECRET"
    ):
        raise RuntimeError(
            "JWT_SECRET_KEY no está configurada correctamente."
        )

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )