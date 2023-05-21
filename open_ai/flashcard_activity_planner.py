from fastapi import HTTPException, status
from db.models.chat import ActivityType, AgentAnalysis, AgentFlashCardActivity, FlashCard
from open_ai.activity_planner import recover_activity_messages, update_activities

from open_ai.general import check_conversation_exists, check_is_valid_json_and_get_correct_json, json_to_string, get_agent_response, string_to_json

json_format = {
    "incorrect": "incorrect word or phrase", 
    "correct": "correct word or phrase", 
    "flashcard": {
        "sentence": "sentence with a blank space",
        "correct_sentence": "complete sentence with the correct word or phrase", 
        "correct_option": "correct option",
        "options": [
            "correct option", 
            "incorrect option 1", 
            "incorrect option 2", 
            "incorrect option 3"
        ]
    }, 
    "comments": "your extra comments"
}

flashcard_activity_context = "You are an English expert and your job is to generate an appropiate learning flashcard based on the gramatical, "\
"spelling and pronunciation analysis that will be provided to you. "\
"The flashcard should contain an incorrect word or phrase, its correction, a sentence with a blank space that uses the correction, "\
f"and various options for filling in the blank. Flashcard must be in the following JSON format: {json_format}"

def create_flashcard_activity(context_id: str, agent_analysis: AgentAnalysis) -> AgentFlashCardActivity:
    check_conversation_exists(context_id)
    activity_messages = recover_activity_messages(context_id, ActivityType.FLASHCARD)
    agent_messages = []
    if len(activity_messages) == 0:
        agent_messages = [{"role": "system", "content": flashcard_activity_context}]
    else:
        agent_messages.extend(activity_messages[:3])

    agent_analysis_str = json_to_string(dict(agent_analysis))
    user_message = f"Please generate a flashcard based on the following analysis: <{agent_analysis_str}>."

    agent_messages.append({"role": "user", "content": user_message})
    print(f"\n>>>>>>>>>>>>>>>>> [ACTIVITY] Sent messages <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_messages} \n")
    agent_response = get_agent_response(agent_messages)
    print(f"\n>>>>>>>>>>>>>>>>> [ACTIVITY] Received message <<<<<<<<<<<<<<<<<<<\n")
    print(f"{agent_response} \n")

    # Check if chatgpt_response matches with the expected one and the convert it to an object
    max_retries = 1
    retries = 0
    retry_messages = []
    retry_messages.extend(agent_messages)
    valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
    while (not valid_json) and (retries < max_retries):
        print(f"\n>>>>>>>>>>>>>>>>> [ACTIVITY] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{retry_messages} \n")
        retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
        agent_response = get_agent_response(retry_messages)
        print(f"\n>>>>>>>>>>>>>>>>> [ACTIVITY] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        retries += 1

    if retries == max_retries and not valid_json:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

    agent_response_json = string_to_json(agent_response)
    agent_messages.append({"role": "assistant", "content": agent_response_json})
    update_activities(context_id, agent_messages, ActivityType.FLASHCARD)

    flashcard = FlashCard(**agent_response_json['flashcard'])
    
    agent_response_json['flashcard'] = flashcard
    '''print(f"agent_response_json: {agent_response_json}")
    print(f"agent_response_json incorrect: {agent_response_json['incorrect']}")
    print(f"agent_response_json correct: {agent_response_json['correct']}")
    print(f"agent_response_json flashcard: {agent_response_json['flashcard']}")
    print(f"agent_response_json comments: {agent_response_json['comments']}")'''

    '''return AgentFlashCardActivity(
        incorrect=agent_response_json['incorrect'],
        correct=agent_response_json['correct'], 
        flashcard=agent_response_json['flashcard'],
        comments=agent_response_json['comments'],
    )'''
    return AgentFlashCardActivity(**agent_response_json)