from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from db.models.user import User
from users.auth import get_current_user, generate_access_token
from users.finder import search_user_db, user_exists_by_email
from users.password import password_matches

router = APIRouter(prefix='/auth', tags=["auth"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_exists = user_exists_by_email(form.username)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user_db = search_user_db("email", form.username)
    if not password_matches(form.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña no es correcta')

    access_token = generate_access_token(user_db)

    return { 'access_token': access_token, 'token_type': 'bearer'}

@router.get('/me')
def me(user: User = Depends(get_current_user)):
    return user

