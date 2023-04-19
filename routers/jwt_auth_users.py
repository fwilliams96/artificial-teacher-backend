from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #minutes
SECRET = 'ff85a2d074688ee05503a2c5a470683813948cd5b03227b593fff99753efbd14' # openssl rand -hex 32 (ubuntu)

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=['bcrypt'])

# Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    'mouredev': {
        'username': 'mouredev',
        'full_name': 'Brais Moure',
        'email': 'braismoure@mourede.com',
        'disabled': False,
        'password': '$2a$12$rbGx9/HOBAZ9AyjNFzcVR.E/TGE7oo5V1fX0oHRtjhYTjhdrF2Meq'
    },
    'mouredev2': {
        'username': 'mouredev2',
        'full_name': 'Brais Moure 2',
        'email': 'braismoure2@mourede.com',
        'disabled': True,
        'password': '$2a$12$7DAEJL1Gs17WsJA9Skpn7Oq4ICKh04cvoxLLLcmynO2Fa/yHiFuyG'
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def authenticated_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales incorrectas', headers={'WWW-Authenticate': 'Bearer'})

    try:
        user = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = user.get('sub')
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario está inactivo')
    return user

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña no es correcta')
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {
        'sub': user.username,
        'exp': expire
    }

    return { 'access_token': jwt.encode(access_token, SECRET, algorithm=ALGORITHM), 'token_type': 'bearer'}

@router.get('/user/me')
async def me(user: User = Depends(current_user)):
    return user
