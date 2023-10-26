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

    job_interview_context = "You are a job interviewer for a tech company called Ash Technologies and your job is to ask all the basic details of the interviewed"\
    f"like the age, experience, why is the appropiate person, etc. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    buy_supermarket_context = "You are a cashier called Elliot from Miranda supermarket and your job is to attend a person who is going to pay. "\
    f"Summarize the products passed by the customer (make them up) and ask if they are going to pay in cash or card, etc. "\
    f"Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    checkin_airport_context = "You are the person in charge of airport check-in and your job is to ask the personal information needed for the flight, "\
    f"like the full name, age, destination, etc. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    order_food_context = "You are a waiter from the restaurant Sajarel and your job is to ask which menu is the client going to ask, if him/her is going to have "\
    f"water, soft drink, which drink will be, etc. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    checkin_accommodation_context = "You are the recepcionist of the hotel Patricio and your job is to ask the personal information of the guest, "\
    f"like the full name, how many nights will stay, the number of people, etc. At the end, tell him/her the room number as well. "\
    f"Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    doctor_visit_context = "You are a doctor called Lobezno and your job is to ask the patient the full name, age, all the symptoms the patient has, "\
    f"how many days has been with those symptoms, etc. When you finish, give him/her a medical prescription if it's necessary. "\
    f"Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    travel_agency_context = "You are a flight agent and your job is to find the perfect destination for the client, ask him/her the full name, age and alll "\
    f"the information you consider necessary to recommend a good destination. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    partying_with_strangers_context = "You have assisted to a party with strangers and you saw a girl or a boy that is alone so you approximate to him/her."\
    f"Your job is to ask about him/her full name, age and all the stuff you ask when you are partying. Use a more informal language that includes some modern "\
    f"words or sayings among the youth. Finish the conversation by giving your Instagram. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    urgency_call_police_context = "You are a police station secretary and you suddenly receive a call from someone asking for help. Your job is to ask him/her "\
    f"the full name, age, location, a description of what happened, etc. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    parents_school_meeting = "You are a school tutor and you are having a meeting with the parents of a creature that is having a very bad behaviour at school."\
    f"First of all tell them about the different situations that the school has experienced with the kid. Yor job is to ask the parents about the routine "\
    f"the kid is having at home, if there is any problem at home, etc. Don't take long. The response should follow this JSON format: {json_to_string(json_format)}"

    role_play_generator_assistant = f"{json_to_string(json_example_format)}"

    role_play_user_message_json_format = lambda user_message, is_over: {
        "sentence": user_message,
        "is_over": is_over
    }

    def talk(self, role_play_messages: list[RolePlayMessage], role_play_type: RolePlayType) -> RolePlayMessage:

        if role_play_type == RolePlayType.JOB_INTERVIEW:
            context = self.job_interview_context
        elif role_play_type == RolePlayType.BUY_SUPERMARKET:
            context = self.buy_supermarket_context
        elif role_play_type == RolePlayType.CHECKIN_AIRPORT:
            context = self.checkin_airport_context
        elif role_play_type == RolePlayType.ORDER_FOOD_RESTAURANT:
            context = self.order_food_context
        elif role_play_type == RolePlayType.CHECKIN_ACCOMMODATION:
            context = self.checkin_accommodation_context
        elif role_play_type == RolePlayType.DOCTOR_VISIT:
            context = self.doctor_visit_context
        elif role_play_type == RolePlayType.TRAVEL_AGENCY:
            context = self.travel_agency_context
        elif role_play_type == RolePlayType.PARTYING_WITH_STRANGERS:
            context = self.partying_with_strangers_context
        elif role_play_type == RolePlayType.URGENCY_CALL_POLICE:
            context = self.urgency_call_police_context
        else:
            context = self.parents_school_meeting         

        messages=[{"role": "system", "content": context}]

        for role_play_message in role_play_messages:
            if role_play_message.sender_id is None:
                messages.append({"role": "assistant", "content": json_to_string(ChatgptRolePlayTalker.role_play_user_message_json_format(role_play_message.message, False))})
            else:
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