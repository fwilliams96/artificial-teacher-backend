from fastapi import HTTPException, status
from ai_teacher.users.user_listenings.domain.external_sentence_generator import ExternalSentenceGenerator
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai
from shared.infrastructure.utils.utils import check_is_valid_json_and_get_correct_json, json_to_string, string_to_json

class ChatgptSentenceGenerator(ExternalSentenceGenerator):

    json_format = {
        "sentence": "full sentence", 
        "comments": "your extra comments"
    }

    json_example_format = {
        "sentence": "The cat meowed", 
        "comments": "N/A"
    }

    sentence_writer_context = "You are a sentence writer and your job is to make up short sentences based on a provided topic."\
    f"The response should follow this JSON format: {json_to_string(json_format)}"

    sentence_writer_assistant = f"{json_to_string(json_example_format)}"

    sentence_writer_user_message = lambda topic: "Write a short sentence of 50 characters based on " + topic
     
    def generate(self, topic: str) -> str:
        messages=[{"role": "system", "content": self.sentence_writer_context}]
        messages.append({"role": "user", "content": ChatgptSentenceGenerator.sentence_writer_user_message("cats")})
        messages.append({"role": "assistant", "content": self.sentence_writer_assistant})
        messages.append({"role": "user", "content": ChatgptSentenceGenerator.sentence_writer_user_message(topic)})

        print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        print(f"{messages} \n")
        agent_response = send_messages_to_ai(messages)
        print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Received message <<<<<<<<<<<<<<<<<<<\n")
        print(f"{agent_response} \n")

        max_retries = 1
        retries = 0
        retry_messages = []
        retry_messages.extend(messages)
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        while (not valid_json) and (retries < max_retries):
            print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            print(f"{retry_messages} \n")
            retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
            agent_response = send_messages_to_ai(retry_messages)
            print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            print(f"{agent_response} \n")
            valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
            retries += 1

        if retries == max_retries and not valid_json:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

        agent_response_json = string_to_json(agent_response)
        messages.append({"role": "assistant", "content": agent_response_json})

        return agent_response_json['sentence']
    

