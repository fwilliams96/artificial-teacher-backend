from datetime import datetime
from fastapi import HTTPException, status
from ai_teacher.users.user_role_plays.domain.external_role_play_talker import ExternalRolePlayTalker
from ai_teacher.users.user_role_plays.domain.role_play import RolePlayMessage, RolePlayMessageType, RolePlayType
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai
from shared.infrastructure.utils.utils import check_is_valid_json_and_get_correct_json, json_to_string, string_to_json

class ChatgptRolePlayTalker(ExternalRolePlayTalker):
    
    def __init__(self, ) -> None:
        pass

    json_format = {
        "sentence": "your sentence o question", 
        "is_over": "true if the goal of the role play has been reached or false if it's not reachet yet"
    }

    json_example_format = {
        "sentence": "Hi, this is Williams restaurant, what would you like to have?", 
        "is_over": "false"
    }

    job_interview_context = "You are a job interviewer for a tech company called Miranda and your job is to ask all the basic details of the interviewed"\
    f"like the age, experience, why is the appropiate person, etc. The response should follow this JSON format: {json_to_string(json_format)}"

    role_play_generator_assistant = f"{json_to_string(json_example_format)}"

    role_play_generator_user_message = lambda topic: "Keep a conversation based on the following topic and finished it when you consider the goal has been reached:" + topic

    role_play_user_message_json_format = lambda user_message, is_over: {
        "sentence": user_message,
        "is_over": is_over
    }

    def talk(self, role_play_messages: list[RolePlayMessage], role_play_type: RolePlayType) -> RolePlayMessage:

        context = self.job_interview_context #TODO
        if role_play_type == RolePlayType.JOB_INTERVIEW:
            context = self.job_interview_context

        messages=[{"role": "system", "content": context}]

        #messages.append({"role": "user", "content": ChatgptRolePlayTalker.role_play_generator_user_message("order food restaurant")})
        #messages.append({"role": "assistant", "content": self.role_play_generator_assistant})

        print(role_play_messages)

        for role_play_message in role_play_messages:
            if role_play_message.sender_id is None:
                messages.append({"role": "assistant", "content": json_to_string(ChatgptRolePlayTalker.role_play_user_message_json_format(role_play_message.message, False))})
                #messages.append({"role": "assistant", "content": role_play_message.message})
            else:
                #messages.append({"role": "user", "content": json_to_string(ChatgptRolePlayTalker.role_play_user_message_json_format(role_play_message.message, False))})
                messages.append({"role": "user", "content": role_play_message.message})

        print(f"\n>>>>>>>>>>>>>>>>> [ROLE PLAY TALKER] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        print(f"{messages} \n")
        agent_response = send_messages_to_ai(messages)
        print(f"\n>>>>>>>>>>>>>>>>> [ROLE PLAY TALKER] Received message <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")

        max_retries = 1
        retries = 0
        retry_messages = []
        retry_messages.extend(messages)
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        while (not valid_json) and (retries < max_retries):
            print(f"\n>>>>>>>>>>>>>>>>> [ROLE PLAY TALKER] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            print(f"{retry_messages} \n")
            retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
            agent_response = send_messages_to_ai(retry_messages)
            print(f"\n>>>>>>>>>>>>>>>>> [ROLE PLAY TALKER] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            print(f"{agent_response} \n")
            valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
            retries += 1

        if retries == max_retries and not valid_json:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

        agent_response_json = string_to_json(agent_response)
        messages.append({"role": "assistant", "content": agent_response_json})

        last_message = str(agent_response_json['is_over']).lower() == "true"

        return RolePlayMessage(
            message=agent_response_json['sentence'],
            last_message=last_message,
            role_play_id=role_play_message.role_play_id,
            sender_id=None,
            type=RolePlayMessageType.TEXT,
            sent_date=datetime.now()
        )