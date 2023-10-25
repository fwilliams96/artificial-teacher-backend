import ast
import json
import re

from shared.infrastructure.openai.client.openai_client import send_messages_to_ai

rewrite_context = "You are a JSON validator and your job is to return the JSON "\
"I will give in a proper format, using doble quotes for the fields and single quotes "\
"for the content of them."

def check_is_valid_json_and_get_correct_json(json_string):
    contains_json = check_contains_json(json_string)
    print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - String contains a json?: {contains_json} <<<<<<<<<<<<<<<<<<<\n")
    if not contains_json:
        return False, json_string
    json_string = extract_existing_json(json_string)
    print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - After extracting json: {json_string} <<<<<<<<<<<<<<<<<<<\n")
    #json_string = fix_json_quotes(json_string)
    #print(f"\n>>>>>>>>>>>>>>>>> [VALIDATING] - After fixing json quotes: {json_string} <<<<<<<<<<<<<<<<<<<\n")
    try:
        json.loads(json_string)
        return True, json_string
    except ValueError as e:
        return False, json_string
    
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

def fix_json_quotes(json_string) -> str:
    try:
        obj = ast.literal_eval(json_string)
        return json.dumps(obj)
    except Exception as e:
        print("Literal eval failed, trying to rewrite JSON..")
        return rewrite_json(json_string)
    
def rewrite_json(json: str) -> str:
    agent_messages = [{"role": "system", "content": rewrite_context}]
    user_message = f"Please rewrite the following JSON using the context I gave you before: {json}."
    agent_messages.append({"role": "user", "content": user_message})
    print(f"\n>>>>>>>>>>>>>>>>> [REWRITE] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_messages} \n")
    agent_response = send_messages_to_ai(agent_messages)
    print(f"\n>>>>>>>>>>>>>>>>> [REWRITE] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")
    return agent_response

def string_to_json(json_string: str) -> dict:
    return json.loads(json_string)

def json_to_string(json_dict: dict) -> str:
    return json.dumps(json_dict)