from bson import ObjectId
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution

def map_domain_to_entity(user_description: UserDescription) -> dict:
    return {
        "topic": user_description.topic,
        "user_id": ObjectId(user_description.user_id),
        "finished": user_description.finished,
        "image": user_description.image,
        "user_solution": map_user_solution_to_entity(user_description.user_solution) if user_description.user_solution != None else None,
        "correction": map_correction_to_entity(user_description.correction) if user_description.correction != None else None,
        "routine_id": ObjectId(user_description.routine_id) if user_description.routine_id != None else None
    }

def map_user_solution_to_entity(user_solution: UserSolution) -> dict:
    return {
        "text": user_solution.text
    }

def map_correction_to_entity(correction: UserDescriptionCorrection) -> dict:
    return {
        "description": correction.description,
        "rating": correction.rating,
        "comments": correction.comments    
    }