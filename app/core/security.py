from passlib.context import CryptContext
import time
import jwt
from typing import Any, Dict
from app.core.config import settings

ACCESS_TTL_SECONDS = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALG

# Задаём алгоритм хэширования и автообновление алгоритма
pwd_box = CryptContext(schemes=["bcrypt"], deprecated="auto")

# функция превращения пароля в хэш
def hash_pwd(password: str) -> str:
    return pwd_box.hash(password)
# функция сравнения полученного хэша с хэшом из БД
def verify_pwd(password: str, hash_pwd: str) -> bool:
    return pwd_box.verify(password, hash_pwd)

# функция текущего времени
def _now() -> int:
    return int(time.time())

# функция генерации JWT access token
def create_access_token(sub: str, role: str) -> str:
    payload = {
        "sub": sub,
        "role": role,
        "type": "access",
        "iat": _now(),
        "exp": _now() + ACCESS_TTL_SECONDS,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# функция декодирования токена
def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])