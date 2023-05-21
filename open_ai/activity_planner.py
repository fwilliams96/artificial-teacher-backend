from db.models.chat import ActivityType, MessageType
from db.client import db_client
from bson import ObjectId

from open_ai.general import build_agent_message, recover_all_messages

def recover_last_activity_message_db(context_id: str):
    messages_db = recover_all_messages(context_id)
    activity_messages_db = list(filter(lambda message_db: message_db['type'] == MessageType.ACTIVITY.value, messages_db))
    if len(activity_messages_db) == 0:
        return None
    return activity_messages_db[-1]

def recover_activity_messages_db(context_id: str, activity_type: ActivityType):
    messages_db = recover_all_messages(context_id)
    activity_messages_db = list(filter(lambda message_db: message_db['type'] == MessageType.ACTIVITY.value, messages_db))
    return list(filter(lambda activity_message_db: activity_message_db['message']['activity_type'] == activity_type.value, activity_messages_db))

def recover_activity_messages(context_id: str, activity_type: ActivityType):
    activity_messages_db = recover_activity_messages_db(context_id, activity_type)
    return [build_agent_message(activity_message_db) for activity_message_db in activity_messages_db]

def update_activities(context_id: str, activity_messages: list, activity_type: ActivityType):
    activity_messages_db = [build_db_activity_message(activity_message, activity_type) for activity_message in activity_messages]
    update_operation = {"$push": {"messages": {"$each": activity_messages_db}}}
    db_client.conversations.update_one({"_id": ObjectId(context_id)}, update_operation)
    '''activity_messages_db = [build_db_activity_message(activity_message, activity_type) for activity_message in activity_messages]
    messages_db = recover_all_messages(context_id)
    messages_db.extend(activity_messages_db)
    conversation = {
        "messages": messages_db
    }
    db_client.conversations.find_one_and_replace({"_id": ObjectId(context_id)}, conversation)'''

def build_db_activity_message(message: dict, activity_type: ActivityType):
    return {
        'type': MessageType.ACTIVITY.value,
        'message': {
            'role': message['role'],
            'content': message['content'],
            'activity_type': activity_type.value
        }
    }

