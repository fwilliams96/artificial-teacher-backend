from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.models.user import User, UserDb
from users.finder import search_user
from jose import jwt, JWTError
from datetime import datetime, timedelta

oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 480 #minutes
SECRET = 'ff85a2d074688ee05503a2c5a470683813948cd5b03227b593fff99753efbd14' # openssl rand -hex 32 (ubuntu)

def generate_access_token(user_db: UserDb) -> str:
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {
        'sub': user_db.email,
        'exp': expire
    }

    return jwt.encode(access_token, SECRET, algorithm=ALGORITHM)


def get_authenticated_user(token: str = Depends(oauth2)) -> User:
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales incorrectas', headers={'WWW-Authenticate': 'Bearer'})
    try:
        user = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email = user.get('sub')
        if email is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user("email", email)

def get_current_user(user: User = Depends(get_authenticated_user)) -> User:
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario está inactivo')
    return user