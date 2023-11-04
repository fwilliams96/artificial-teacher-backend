from fastapi import HTTPException, status
from ai_teacher.activities.flashcard.domain.external_flashcard_generator import ExternalFlashcardGenerator
from ai_teacher.activities.flashcard.domain.flashcard import FlashCard
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai
from shared.infrastructure.utils.utils import check_is_valid_json_and_get_correct_json, json_to_string, string_to_json

class ChatgptFlashcardGenerator(ExternalFlashcardGenerator):

    json_format = {
        "incomplete_sentence": "sentence with a blank space",
        "correct_sentence": "complete sentence with the correct word or phrase", 
        "correct_option": "correct option",
        "wrong_options": [
            "incorrect option 1", 
            "incorrect option 2", 
            "incorrect option 3"
        ],
        "comment": "any additional comment"
    }

    sentence_analysis_example = {
        "type": "GRAMMAR",
        "errors": ["It's a future sentence, it should use 'I will play'"],
        "comment": "N/A"
    }

    json_example_format = {
        "incomplete_sentence": "I _ play football tomorrow",
        "correct_sentence": "I will play football tomorrow", 
        "correct_option": "will",
        "wrong_options": [
            "have", 
            "am"
        ],
        "comment": "N/A"
    }

    flashcard_generator_context = "You are an English expert and your job is to generate an appropiate learning flashcard based on the gramatical or "\
    "spelling analysis that will be provided to you. "\
    "The flashcard should contain an incomplete sentence with a missing word that has to be filled, the full correct sentence, the correct option that fits the incomplete sentence and various other wrong options."\
    f"The response must follow this JSON format: {json_format}"

    flashcard_generator_assistant = f"{string_to_json(json_example_format)}"

    flashcard_generator_user_message = lambda sentence: "Please analyze the following sentence: " + sentence

    def generate(self, sentence_analysis: SentenceAnalysis) -> FlashCard:
        messages=[{"role": "system", "content": self.flashcard_generator_context}]
        messages.append({"role": "user", "content": ChatgptFlashcardGenerator.flashcard_generator_user_message(json_to_string(self.sentence_analysis_example))})
        messages.append({"role": "assistant", "content": self.flashcard_generator_assistant})
        messages.append({"role": "user", "content": ChatgptFlashcardGenerator.flashcard_generator_user_message(json_to_string(self.sentence_analysis_to_json(sentence_analysis)))})

        #print(f"\n>>>>>>>>>>>>>>>>> [FLASHCARD GENERATOR] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        #print(f"{messages} \n")
        agent_response = send_messages_to_ai(messages)
        #print(f"\n>>>>>>>>>>>>>>>>> [FLASHCARD GENERATOR] Received message <<<<<<<<<<<<<<<<<<<\n")
        #print(f"{agent_response} \n")

        max_retries = 1
        retries = 0
        retry_messages = []
        retry_messages.extend(messages)
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        while (not valid_json) and (retries < max_retries):
            #print(f"\n>>>>>>>>>>>>>>>>> [FLASHCARD GENERATOR] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            #print(f"{retry_messages} \n")
            retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
            agent_response = send_messages_to_ai(retry_messages, 50)
            #print(f"\n>>>>>>>>>>>>>>>>> [FLASHCARD GENERATOR] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            #print(f"{agent_response} \n")
            valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
            retries += 1

        if retries == max_retries and not valid_json:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

        agent_response_json = string_to_json(agent_response)
        messages.append({"role": "assistant", "content": agent_response_json})

        return FlashCard(
            incomplete_sentence=agent_response_json['incomplete_sentence'],
            correct_sentence=agent_response_json['correct_sentence'],
            correct_option=agent_response_json['correct_option'],
            wrong_options=[wrong_option for wrong_option in agent_response_json['wrong_options']]
        )
    
    def sentence_analysis_to_json(sentence_analysis: SentenceAnalysis) -> dict:
        return {
            "type": sentence_analysis.type,
            "errors": [error for error in sentence_analysis.errors],
            "comment": sentence_analysis.comment
        }