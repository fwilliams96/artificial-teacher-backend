
import random
from fastapi import HTTPException, status
from db.models.user import User
from open_ai.general import check_is_valid_json_and_get_correct_json, get_agent_response, json_to_string, string_to_json
from open_ai.preference import get_user_preferences

json_format = {
    "topic": "random topic", 
    "comments": "your extra comments"
}

json_example_format = {
    "topic": "Videogames", 
    "comments": "Nowdays, videogames is a popular topic among young people"
}

topic_planner_context = "Tell me a random topic we can use to keep a discussion between an English speaker and a learner."
f"To respond, use the following this JSON format: {json_to_string(json_format)}"

topic_planner_assistant = f"{json_to_string(json_example_format)}"

topic_planner_user_message = "Tell me a random topic"

def get_random_user_preference(user: User) -> str:
    user_preferences = get_user_preferences(user)
    random_user_preference = random.choice(user_preferences)
    return random_user_preference.preference

def get_random_topic() -> str:
    messages = []
    messages=[{"role": "system", "content": topic_planner_context}]
    messages.append({"role": "user", "content": topic_planner_user_message})
    messages.append({"role": "assistant", "content": topic_planner_assistant})
    messages.append({"role": "user", "content": topic_planner_user_message})

    print(f"\n>>>>>>>>>>>>>>>>> [RANDOM TOPIC] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{messages} \n")
    agent_response = get_agent_response(messages, 50)
    print(f"\n>>>>>>>>>>>>>>>>> [RANDOM TOPIC] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")

    max_retries = 1
    retries = 0
    retry_messages = []
    retry_messages.extend(messages)
    valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
    while (not valid_json) and (retries < max_retries):
        print(f"\n>>>>>>>>>>>>>>>>> [RANDOM TOPIC] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        print(f"{retry_messages} \n")
        retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
        agent_response = get_agent_response(retry_messages, 50)
        print(f"\n>>>>>>>>>>>>>>>>> [RANDOM TOPIC] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        retries += 1

    if retries == max_retries and not valid_json:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

    agent_response_json = string_to_json(agent_response)
    return agent_response_json["topic"]