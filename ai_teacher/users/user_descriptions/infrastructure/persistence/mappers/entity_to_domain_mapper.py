from ai_teacher.users.user_descriptions.domain.user_description import ImageDescription, UserDescription, UserDescriptionCorrection, UserSolution, UserSolutionType

def map_entity_to_domain(user_description: dict) -> UserDescription:

    return UserDescription(
        id=str(user_description["_id"]),
        topic=user_description["topic"],
        user_id=str(user_description["user_id"]),
        finished=user_description["finished"],
        image=user_description["image"],
        image_id=user_description["image_id"],
        user_solution=map_user_solution_to_domain(user_description["user_solution"]) if user_description["user_solution"] != None else None,
        correction=map_correction_to_domain(user_description["correction"]) if user_description["correction"] != None else None,
        routine_id=str(user_description["routine_id"]) if user_description["routine_id"] != None else None,
    )

def map_user_solution_to_domain(user_solution: dict) -> UserSolution:
    return UserSolution(
        content=user_solution["content"],
        type=UserSolutionType[str(user_solution["type"]).upper()]
    )

def map_correction_to_domain(correction: dict) -> UserDescriptionCorrection:
    return UserDescriptionCorrection(
        comments=correction["comments"],
        rating=correction["rating"],
        description=correction["description"]
    )

def map_image_description_to_domain(image_description: dict) -> ImageDescription:
    return ImageDescription(
        id=str(image_description["_id"]),
        image=image_description["image"],
        topic=image_description["topic"]
    )