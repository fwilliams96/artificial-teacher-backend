from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ai_teacher.users.shared.application.user_finder import UserFinder
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from ai_teacher.users.shared.domain.user import User, UserDb

crypt = CryptContext(schemes=['bcrypt'])
user_finder = UserFinder()
oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 480 #minutes
SECRET = 'ff85a2d074688ee05503a2c5a470683813948cd5b03227b593fff99753efbd14' # openssl rand -hex 32 (ubuntu)

def encrypt_password(password: str) -> str:
    return crypt.hash(password)

def password_matches(form_password: str, db_password: str) -> bool:
    return crypt.verify(form_password, db_password)

def generate_access_token(user_db: UserDb) -> str:
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {
        'sub': user_db.email,
        'exp': expire
    }

    return jwt.encode(access_token, SECRET, algorithm=ALGORITHM)


def get_authenticated_user(token: str = Depends(oauth2)) -> UserDb | None:
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales incorrectas', headers={'WWW-Authenticate': 'Bearer'})
    try:
        user = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = user.get('sub')
        if email is None:
            raise exception
        
    except JWTError:
        raise exception
    return user_finder.find_user_by_email(email)

def get_current_user(user: UserDb = Depends(get_authenticated_user)) -> UserDb:
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario está inactivo')
    return user