from passlib.context import CryptContext


HASHING_ALGORITHM = "bcrypt"

password_context = CryptContext(schemes=[HASHING_ALGORITHM], deprecated="auto")

def get_password_hash(password):
    return password_context.hash(password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)