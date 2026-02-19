import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_EXPIRES

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
