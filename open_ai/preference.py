from bson import ObjectId
from fastapi import HTTPException, status
from db.models.preference import Preference, UserPreference
from db.models.user import User
from db.client import db_client
from db.schemas.preference import preference_schema, user_preference_schema

def create_preference_db(preference: Preference) -> Preference:
    preference_db = build_preference_db(preference)
    preference_id = str(db_client.preferences.insert_one(preference_db).inserted_id)
    preference.id = preference_id
    return preference

def create_user_preference_db(user: User, user_preference: UserPreference) -> UserPreference:

    preference_db = db_client.preferences.find_one({"_id": ObjectId(user_preference.preference_id)})

    if preference_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Preference not found.")

    user_preference.user_id = user.id
    user_preference.preference = preference_db["preference"]
    user_preference_db = build_user_preference_db(user_preference)
    user_preference_id = str(db_client.user_preferences.insert_one(user_preference_db).inserted_id)
    user_preference.id = user_preference_id
    return user_preference

def get_preferences_db() -> list[Preference]:
    preferences_db = db_client.preferences.find()
    return [build_preference(preference_db) for preference_db in preferences_db]

def get_user_preferences(user: User) -> list[UserPreference]:
    user_preferences_db = db_client.user_preferences.find({"user_id": ObjectId(user.id)})
    user_preferences = [build_user_preference(user_preference_db) for user_preference_db in user_preferences_db]

    for user_preference in user_preferences:
        preference_db = db_client.preferences.find_one({"_id": ObjectId(user_preference.preference_id)})
        user_preference.preference = preference_db["preference"]

    return user_preferences

def build_preference_db(preference: Preference) -> dict:
    return {
        "preference": preference.preference
    }

def build_user_preference_db(user_preference: UserPreference) -> dict:
    return {
        "preference_id": ObjectId(user_preference.preference_id),
        "user_id": ObjectId(user_preference.user_id)
    }

def build_preference(preference_db: dict) -> Preference:
    preference_db_schema = preference_schema(preference_db)
    return Preference(
        id=preference_db_schema["id"],
        preference=preference_db_schema['preference']
    )

def build_user_preference(user_preference: dict) -> UserPreference:
    user_preference_db_schema = user_preference_schema(user_preference)
    return UserPreference(
        id=user_preference_db_schema["id"],
        preference_id=user_preference_db_schema['preference_id'],
        user_id=user_preference_db_schema['user_id']
    )