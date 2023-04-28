from db.models.user import User, UserDb
from db.client import db_client
from db.schemas.user import user_schema, userdb_schema
from bson import ObjectId

def user_exists_by_id(id: str) -> bool:
    user = search_user("_id", ObjectId(id))
    return user != None

def user_exists_by_email(email: str) -> bool:
    user = search_user("email", email)
    return user != None

def search_user(key: str, value: any) -> User:
    try:
        user = db_client.users.find_one({key:value})
        return User(**user_schema(user))
    except:
        return None

def search_user_db(key: str, value: any) -> UserDb:
    try:
        user_db = db_client.users.find_one({key:value})
        return UserDb(**userdb_schema(user_db))
    except:
        return None