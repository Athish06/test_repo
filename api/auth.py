import bcrypt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET", "a_very_secure_random_secret_key_123456789")

def hash_password(password: str):
    # FIXED: Use bcrypt for secure hashing
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_jwt_token(user_id):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None