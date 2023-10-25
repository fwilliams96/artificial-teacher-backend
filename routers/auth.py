from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ai_teacher.users.shared.application.user_auth import get_current_user, password_matches, generate_access_token
from ai_teacher.users.shared.application.user_finder import UserFinder
from ai_teacher.users.shared.domain.user import UserDb, User

router = APIRouter(prefix='/auth', tags=["auth"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = UserFinder().find_user_by_email(form.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    if not password_matches(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña no es correcta')

    access_token = generate_access_token(user)

    return {
        'access_token': access_token, 
        'token_type': 'bearer'
    }

@router.get('/me')
def me(user: UserDb = Depends(get_current_user)):
    return User(
        id=user.id,
        disabled=user.disabled,
        email=user.email
    )

