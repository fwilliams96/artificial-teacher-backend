def preference_schema(preference) -> dict:
    return {
        "id": str(preference["_id"]),
        "preference": preference["preference"]
    }

def user_preference_schema(preference) -> dict:
    return {
        "id": str(preference["_id"]),
        "preference_id": str(preference["preference_id"]),
        "user_id": str(preference["user_id"]),
    }