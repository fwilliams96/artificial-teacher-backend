from typing import Tuple
from db.client import db_client
from bson import ObjectId
from db.models.chat import MessageType

from open_ai.general import check_conversation_exists, recover_all_messages, get_agent_response

talker_context = "You are an English expert and your job is to keep a conversation with a user in a basic level, "\
"I will be your man in the middle. Keep the conversation active, focusing on learning English."

def start_conversation(user_message: str) -> Tuple[str, str]:
    messages=[{"role": "system", "content": talker_context}] 
    messages.append({"role": "user", "content": user_message})
    agent_response = get_agent_response(messages)
    messages.append({"role": "assistant", "content": agent_response})
    context_id = create_conversation_and_get_context_id(messages)
    return context_id, agent_response

def create_conversation_and_get_context_id(conversation_messages: list[dict]) -> str:
    conversation_messages_db = [build_db_conversation_message(conversation_message) for conversation_message in conversation_messages]
    conversation = {
        "messages": conversation_messages_db
    }
    return str(db_client.conversations.insert_one(conversation).inserted_id)

def build_db_conversation_message(message: dict):
    return {
        'type': MessageType.CONVERSATION.value,
        'message': {
            'role': message['role'],
            'content': message['content']
        }
    }

def answer_message(context_id: str, user_message: str) -> str:
    check_conversation_exists(context_id)
    messages = recover_conversation_messages(context_id)
    new_messages = []
    new_messages.append({"role": "user", "content": user_message})
    messages.extend(new_messages)
    agent_response = get_agent_response(messages)
    new_messages.append({"role": "assistant", "content": agent_response})
    context_id = update_conversation(context_id, new_messages)
    return agent_response

def recover_conversation_messages_db(context_id: str):
    messages_db = recover_all_messages(context_id)
    return list(filter(lambda message_db: message_db['type'] == MessageType.CONVERSATION.value, messages_db))

def recover_conversation_messages(context_id: str):
    conversation_messages_db = recover_conversation_messages_db(context_id)
    return [build_conversation_message(conversation_message_db) for conversation_message_db in conversation_messages_db]

def build_conversation_message(conversation_message_db: dict):
    return {
        'role': conversation_message_db['message']['role'],
        'content': conversation_message_db['message']['content']
    }

def update_conversation(context_id: str, conversation_messages: list):
    conversation_messages_db = [build_db_conversation_message(conversation_message) for conversation_message in conversation_messages]
    messages_db = recover_all_messages(context_id)
    messages_db.extend(conversation_messages_db)
    conversation = {
        "messages": messages_db
    }
    db_client.conversations.find_one_and_replace({"_id": ObjectId(context_id)}, conversation)
