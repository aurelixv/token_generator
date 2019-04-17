import hashlib
import random
from datetime import datetime

def hash_password(password):
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return str(hashed_password)

def verify_password(password, hashed_password, salt):
    password = hash_password(password)
    if hash_password(password + salt) == hashed_password:
        return 1
    return 0

def salt_generator():
    return hash_password(str(random.random()*(10^4)))
    
def generate_tokens(seed):
    time = hash_password(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
    token = hash_password(seed + time)
    tokens = []
    for _ in range(10):
        token = hash_password(token) 
        tokens.append(token[:6])
    return tokens
