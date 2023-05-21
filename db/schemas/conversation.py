def conversation_schema(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "messages": messages_chema(conversation["messages"])
    }

def messages_chema(messages) -> list:
    return [message_chema(message) for message in messages] 

def message_chema(message: dict) -> dict:
    activity_type = None
    if "activity_type" in message['message']:
        activity_type = message['message']['activity_type']
    return {
        "type": message["type"],
        "message": {
            "role": str(message["message"]["role"]),
            "content": message["message"]["content"],
            "activity_type": activity_type
        }
    }