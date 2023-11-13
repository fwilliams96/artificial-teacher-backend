from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution

def map_entity_to_domain(user_description: dict) -> UserDescription:

    return UserDescription(
        id=str(user_description["_id"]),
        topic=user_description["topic"],
        user_id=str(user_description["user_id"]),
        finished=user_description["finished"],
        image=user_description["image"],
        user_solution=map_user_solution_to_domain(user_description["user_solution"]) if user_description["user_solution"] != None else None,
        correction=map_correction_to_domain(user_description["correction"]) if user_description["correction"] != None else None,
        routine_id=str(user_description["routine_id"]) if user_description["routine_id"] != None else None,
    )

def map_user_solution_to_domain(user_solution: dict) -> UserSolution:
    return UserSolution(
        text=user_solution["text"]
    )

def map_correction_to_domain(correction: dict) -> UserDescriptionCorrection:
    return UserDescriptionCorrection(
        comments=correction["comments"],
        rating=correction["rating"],
        description=correction["description"]
    )