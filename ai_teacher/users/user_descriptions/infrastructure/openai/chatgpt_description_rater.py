from ai_teacher.users.user_descriptions.domain.external_description_rater import ExternalDescriptionRater
from ai_teacher.users.user_descriptions.domain.user_description import UserDescription, UserDescriptionCorrection, UserSolution
from shared.infrastructure.openai.client.openai_client import interpret_image
from shared.infrastructure.utils.utils import json_to_string, string_to_json

class ChatgptDescriptionRater(ExternalDescriptionRater):

    json_format = {
        "rating": "your description rating from 0 to 10", 
        "comments": "your improvement tips or your congratulations",
        "description": "your example of description"
    }

    description_rater_prompt = f"Rate the following description of the attached image from 0 to 10. The response should follow this JSON format: {json_to_string(json_format)}"
     
    def rate(self, user_description: str, image: str) -> UserDescriptionCorrection:
        messages= [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ChatgptDescriptionRater.description_rater_prompt
                    },
                    {
                        "type": "text",
                        "text": user_description
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image
                        }
                    }
                ]
            }
        ]
        agent_response = interpret_image(messages)
        agent_response_json = string_to_json(agent_response)
        #print(agent_response_json)

        return UserDescriptionCorrection(
            rating=agent_response_json["rating"],
            description=agent_response_json["description"],
            comments=agent_response_json["comments"]
        )
    

