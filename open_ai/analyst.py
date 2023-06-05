from fastapi import HTTPException, status
from db.client import db_client
from bson import ObjectId
from db.models.chat import AgentAnalysis, MessageType

from open_ai.general import build_agent_message, check_conversation_exists, check_is_valid_json_and_get_correct_json, recover_free_chat_messages, get_agent_response, string_to_json

json_format = {
    "grammatical_errors": ["list of grammatical errors"], 
    "spelling_errors": ["list of spelling errors"], 
    "pronunciation_errors": ["list of pronunciation errors"], 
    "comments": "your extra comments"
}

analysis_context = "You are an English expert and your job is to analyze the sentences I will provide you. "\
f"Identify any grammatical, spelling, or pronunciation errors and return them in the following JSON format: {json_format}."

def analyze_message(context_id: str, user_message: str) -> AgentAnalysis:
    check_conversation_exists(context_id)
    analysis_messages = recover_analysis_messages(context_id)
    agent_messages = []
    if len(analysis_messages) == 0:
        agent_messages = [{"role": "system", "content": analysis_context}]
    else:
        #[analysis_messages[0], analysis_messages[-2], analysis_messages[-1]]
        agent_messages.extend(analysis_messages[:3])
    user_message = f"Please analyze the following input: <{user_message}>."

    agent_messages.append({"role": "user", "content": user_message})
    print(f"\n>>>>>>>>>>>>>>>>> [ANALYSIS] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_messages} \n")
    agent_response = get_agent_response(agent_messages)
    print(f"\n>>>>>>>>>>>>>>>>> [ANALYSIS] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")

    # Check if chatgpt_response matches with the expected one and the convert it to an object
    max_retries = 1
    retries = 0
    retry_messages = []
    retry_messages.extend(agent_messages)
    valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
    while (not valid_json) and (retries < max_retries):
        print(f"\n>>>>>>>>>>>>>>>>> [ANALYSIS] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{retry_messages} \n")
        retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
        agent_response = get_agent_response(retry_messages)
        print(f"\n>>>>>>>>>>>>>>>>> [ANALYSIS] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        retries += 1
    
    if retries == max_retries and not valid_json:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

    agent_response_json = string_to_json(agent_response)
    agent_messages.append({"role": "assistant", "content": agent_response_json})
    update_analysis(context_id, agent_messages)
    return AgentAnalysis(**agent_response_json)

def recover_analysis_messages_db(context_id: str):
    messages_db = recover_free_chat_messages(context_id)
    return list(filter(lambda message_db: message_db['type'] == MessageType.ANALYSIS.value, messages_db))

def recover_analysis_messages(context_id: str):
    activity_messages_db = recover_analysis_messages_db(context_id)
    return [build_agent_message(activity_message_db) for activity_message_db in activity_messages_db]

def build_db_analysis_message(message: dict):
    return {
        'type': MessageType.ANALYSIS.value,
        'message': {
            'role': message['role'],
            'content': message['content']
        }
    }

def update_analysis(context_id: str, analysis_messages: list):
    analysis_messages_db = [build_db_analysis_message(analysis_message) for analysis_message in analysis_messages]
    update_operation = {"$push": {"messages": {"$each": analysis_messages_db}}}
    db_client.conversations.update_one({"_id": ObjectId(context_id)}, update_operation)

    '''analysis_messages_db = [build_db_analysis_message(analysis_message) for analysis_message in analysis_messages]
    messages_db = recover_all_messages(context_id)
    messages_db.extend(analysis_messages_db)
    conversation = {
        "messages": messages_db
    }
    db_client.conversations.find_one_and_replace({"_id": ObjectId(context_id)}, conversation)'''