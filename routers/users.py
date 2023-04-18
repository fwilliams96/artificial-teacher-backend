from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/users', tags=["users"], responses={404: {"message": "Not found"}})

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="Brais", surname="moure", url="https://moure.dev", age=35),
    User(id=2, name="Fran", surname="fran", url="https://moure.dev", age=33)
]

@router.get('/usersjson')
async def usersjson():
    return [
        { "name": "Brais", "surname": "moure", "url": "https://moure.dev", "age": 35 },
        { "name": "Fran", "surname": "fran", "url": "https://moure.dev", "age": 33 }
    ]
    
# Query param
@router.get('/usersquery')
async def user(id: int):
    return search_user(id)

@router.get('', response_model=list[User], status_code=200)
async def users():
    return users_list

@router.get('/{id}', response_model=User, status_code=200)
async def user(id: int):
    return search_user(id)

@router.post('/', response_model=User, status_code=201)
async def create_user(user: User):
    if (user_exists(user.id)):
        raise HTTPException(status_code=400, detail="User already exists")
    users_list.append(user)
    return user

@router.put('/{id}', status_code=204)
async def update_user(id: int, user: User):
    if (not user_exists(id) or id != user.id):
            raise HTTPException(status_code=404, detail="User does not exist")
    
    for index, savedUser in enumerate(users_list):
        if savedUser.id == id:
            users_list[index] = user

    return user

@router.delete('/{id}', status_code=204)
async def delete_user(id: int):
    if (not user_exists(id)):
        raise HTTPException(status_code=404, detail="User does not exist")
    user = search_user(id)
    for index, savedUser in enumerate(users_list):
        if savedUser.id == id:
            del users_list[index]

    return user

def search_user(id: int):
    users = list(filter(lambda user: user.id == id, users_list))
    try:
        return list(users)[0]
    except:
        return { "error": "Not found" }

def user_exists(id: int):
    users = list(filter(lambda user: user.id == id, users_list))
    return len(users) > 0
