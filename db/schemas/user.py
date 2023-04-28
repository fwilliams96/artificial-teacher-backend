def user_schema(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "disabled": user["disabled"]
    }

def userdb_schema(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
        "disabled": user["disabled"]
    }

def users_chema(users: list[dict]) -> list[dict]:
    return [user_schema(user) for user in users] 