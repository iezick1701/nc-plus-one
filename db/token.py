import os
import jwt 
from datetime import datetime, timezone, timedelta
ALGORITHM = "HS256"


def get_secret():
    secret = os.getenv("JWT_SECRET_KEY")
    return secret


def create_access_token(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)