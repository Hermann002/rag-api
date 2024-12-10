import logging

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Configuration du logger
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

import hashlib

import bcrypt

def hash_password(password: str) -> str:
   hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')

# Usage example
def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw("MySecretPassword".encode("utf-8"), hashed_password.encode("utf-8"))