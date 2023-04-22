def conversation_schema(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "messages": messages_chema(conversation["messages"])
    }

def messages_chema(messages) -> list:
    return [message_chema(message) for message in messages] 

def message_chema(message) -> dict:
    return {
        "role": str(message["role"]),
        "content": message["content"]
    }