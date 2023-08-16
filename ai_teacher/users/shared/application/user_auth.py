from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ai_teacher.users.shared.application.user_finder import UserFinder
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from ai_teacher.users.shared.domain.user import User, UserDb

class UserAuth:

    def __init__(self, user_finder = UserFinder(), crypt = CryptContext(schemes=['bcrypt'])) -> None:
        self.user_finder = user_finder
        self.crypt = crypt

    oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_DURATION = 480 #minutes
    SECRET = 'ff85a2d074688ee05503a2c5a470683813948cd5b03227b593fff99753efbd14' # openssl rand -hex 32 (ubuntu)

    def encrypt_password(self, password: str) -> str:
        return self.crypt.hash(password)
    
    def password_matches(self, form_password: str, db_password: str) -> bool:
        return self.crypt.verify(form_password, db_password)

    def generate_access_token(self, user_db: UserDb) -> str:
        access_token_expiration = timedelta(minutes=self.ACCESS_TOKEN_DURATION)
        expire = datetime.utcnow() + access_token_expiration

        access_token = {
            'sub': user_db.email,
            'exp': expire
        }

        return jwt.encode(access_token, self.SECRET, algorithm=self.ALGORITHM)


    def get_authenticated_user(self, token: str = Depends(oauth2)) -> User | None:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales incorrectas', headers={'WWW-Authenticate': 'Bearer'})
        try:
            user = jwt.decode(token, self.SECRET, algorithms=[self.ALGORITHM])
            email = user.get('sub')
            if email is None:
                raise exception
            
        except JWTError:
            raise exception
        
        return self.user_finder.find_user_by_email(email)

    def get_current_user(self, user: User = Depends(get_authenticated_user)) -> User:
        if user.disabled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario está inactivo')
        return user