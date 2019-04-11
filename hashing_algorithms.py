import hashlib

def hash_password(password, salt):
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    hashed_salt = hashlib.sha512(str(salt).encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha512(
        str(hashed_password).encode('utf-8') + str(hashed_salt).encode('utf-8')
        ).hexdigest()
    return str(hashed_password)

def verify_password(password, hashed_password, salt):
    password = hash_password(password, salt)
    if password == hashed_password:
        return 1
    return 0
    