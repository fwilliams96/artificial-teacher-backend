from bson import ObjectId
from ai_teacher.users.user_descriptions.domain.user_description import ImageDescription, UserDescription, UserDescriptionCorrection, UserSolution

def map_domain_to_entity(user_description: UserDescription) -> dict:
    return {
        "topic": user_description.topic,
        "user_id": ObjectId(user_description.user_id),
        "finished": user_description.finished,
        "image": user_description.image,
        "image_id": user_description.image_id,
        "user_solution": map_user_solution_to_entity(user_description.user_solution) if user_description.user_solution != None else None,
        "correction": map_correction_to_entity(user_description.correction) if user_description.correction != None else None,
        "routine_id": ObjectId(user_description.routine_id) if user_description.routine_id != None else None
    }

def map_user_solution_to_entity(user_solution: UserSolution) -> dict:
    return {
        "content": user_solution.content,
        "type": user_solution.type
    }

def map_correction_to_entity(correction: UserDescriptionCorrection) -> dict:
    return {
        "description": correction.description,
        "rating": correction.rating,
        "comments": correction.comments    
    }

def map_image_description_to_entity(image_description: ImageDescription) -> dict:
    return {
        "topic": image_description.topic,
        "image": image_description.image
    }