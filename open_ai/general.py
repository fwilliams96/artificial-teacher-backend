import json
import re
from bson import ObjectId
from fastapi import HTTPException, status
import openai
from db.schemas.conversation import conversation_schema
from openai_config import API_KEY
from db.client import db_client
import ast

openai.api_key = API_KEY

rewrite_context = "You are a JSON validator and your job is to return the JSON "\
"I will give in a proper format, using doble quotes for the fields and single quotes "\
"for the content of them."

def get_agent_response(messages: list[dict], max_tokens = 4096) -> str:
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
        response_content = response.choices[0].message.content
        return response_content
    except openai.error.RateLimitError:
        print(f"Your user has exceed the quota")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")
    except Exception as e:
        print(f"Exception calling chatgpt: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exception calling chatgpt")

def check_conversation_exists(context_id: str):
    conversation_db = db_client.conversations.find_one({"_id": ObjectId(context_id)})
    if not conversation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Context not found")

def recover_free_chat_messages(context_id: str) -> list:
    conversation_db = db_client.conversations.find_one({"_id": ObjectId(context_id)})
    if not conversation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Free chat not found")
    conversation = conversation_schema(conversation_db)
    return conversation['messages']

def check_is_valid_json_and_get_correct_json(json_string):
    contains_json = check_contains_json(json_string)
    print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - String contains a json?: {contains_json} <<<<<<<<<<<<<<<<<<<\n")
    if not contains_json:
        return False, json_string
    json_string = extract_existing_json(json_string)
    print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - After extracting json: {json_string} <<<<<<<<<<<<<<<<<<<\n")
    json_string = fix_json_quotes(json_string)
    print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - After fixing json quotes: {json_string} <<<<<<<<<<<<<<<<<<<\n")
    try:
        json.loads(json_string)
        return True, json_string
    except ValueError as e:
        return False, json_string
    
def string_to_json(json_string: str) -> dict:
    return json.loads(json_string)

def json_to_string(json_dict: dict) -> str:
    return json.dumps(json_dict)

def build_agent_message(message: dict):
    return {
        'role': message['message']['role'],
        'content': json_to_string(message['message']['content'])
    }

def fix_json_quotes(json_string) -> str:
    try:
        obj = ast.literal_eval(json_string)
        return json.dumps(obj)
    except SyntaxError as e:
        print("Literal eval failed, trying to rewrite JSON..")
        return rewrite_json(json_string)

def check_contains_json(json_string: str):
    exists_json = False
    json_string_regex = re.search(r'(?:```)?(?:json)?\s*({[\s\S]*?})(?:```)?', json_string) #re.search(r"\{.*\}", json_string)
    if json_string_regex:
        exists_json = True
    return exists_json

def extract_existing_json(json_string: str):
    json_string_regex = re.search(r'(?:```)?(?:json)?\s*({[\s\S]*?})(?:```)?', json_string) #re.search(r"\{.*\}", json_string)
    if json_string_regex:
        json_string = json_string_regex.group(0)
    return json_string

def rewrite_json(json: str) -> str:
    agent_messages = [{"role": "system", "content": rewrite_context}]
    user_message = f"Please rewrite the following JSON using the context I gave you before: {json}."
    agent_messages.append({"role": "user", "content": user_message})
    print(f"\n>>>>>>>>>>>>>>>>> [REWRITE] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_messages} \n")
    agent_response = get_agent_response(agent_messages)
    print(f"\n>>>>>>>>>>>>>>>>> [REWRITE] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")
    return agent_response