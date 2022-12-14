from passlib.context import CryptContext

# for hashing, using bcrypt
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_content.hash(password)

