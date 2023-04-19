from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_chema
from bson import ObjectId

router = APIRouter(prefix='/users', tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get('/', response_model=list[User], status_code=status.HTTP_200_OK)
async def users():
    return users_chema(db_client.users.find())

@router.get('/{id}', response_model=User, status_code=status.HTTP_200_OK)
async def user(id: str):
    if not user_exists_by_id(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return search_user("_id", ObjectId(id))

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if (user_exists_by_email(user.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(id: str, user: User):
    if not user_exists_by_id(id) or id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating the user")
    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    if (not user_exists_by_id(id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting the user")

def search_user(key: str, value: any) -> User:
    try:
        user = db_client.users.find_one({key:value})
        return User(**user_schema(user))
    except:
        return { "error": "Not found" }

def user_exists_by_id(id: str):
    user = search_user("_id", ObjectId(id))
    return type(user) == User

def user_exists_by_email(email: str):
    user = search_user("email", email)
    return type(user) == User