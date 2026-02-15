import bcrypt
from typing import Union

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt.checkpw expects bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password: str) -> str:
    # bcrypt.hashpw returns bytes, we decode to store as string
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
