from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, str(hashed_password), scheme="bcrypt")


def get_password_hash(password):
    return pwd_context.hash(password)
