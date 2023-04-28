from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User, UserDb
from db.client import db_client
from db.schemas.user import user_schema
from bson import ObjectId
from users.auth import get_current_user

from users.finder import user_exists_by_email, user_exists_by_id
from users.password import encrypt_password

router = APIRouter(prefix='/users', tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_db: UserDb):
    if (user_exists_by_email(user_db.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user_dict = dict(user_db)
    del user_dict["id"]
    user_dict["disabled"] = False
    user_dict["password"] = encrypt_password(user_dict["password"])

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(id: str, user: User = Depends(get_current_user)):
    if not user_exists_by_id(id) or id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating the user")