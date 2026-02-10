from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):  # works like a function that checks if the provided password matches the stored hashed password. It takes two arguments: the plain text password and the hashed password. It uses the verify method of the pwd_context to compare the two and returns True if they match, or False if they don't.
    return pwd_context.verify(password, hashed_password)