from passlib.context import CryptContext

crypt = CryptContext(schemes=['bcrypt'])

def encrypt_password(form_password: str) -> str:
    return crypt.hash(form_password)

def password_matches(form_password: str, db_password: str) -> bool:
    return crypt.verify(form_password, db_password)
    