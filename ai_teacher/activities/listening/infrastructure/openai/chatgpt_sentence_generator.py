import json
import random
import re
import string

from fastapi import HTTPException, status
from ai_teacher.activities.listening.domain.external_sentence_generator import ExternalSentenceGenerator
from ai_teacher.activities.listening.domain.listening import Sentence, Word
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai
from shared.infrastructure.utils.utils import check_is_valid_json_and_get_correct_json, string_to_json

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
    f"The response should follow this JSON format: {string_to_json(json_format)}"

    sentence_writer_assistant = f"{string_to_json(json_example_format)}"

    sentence_writer_user_message = lambda topic: "Write a short sentence of 50 characters based on " + topic
     
    def generate(self, topic: str) -> Sentence:
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
            agent_response = send_messages_to_ai(retry_messages, 50)
            print(f"\n>>>>>>>>>>>>>>>>> [LISTENING] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            print(f"{agent_response} \n")
            valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
            retries += 1

        if retries == max_retries and not valid_json:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

        agent_response_json = string_to_json(agent_response)
        messages.append({"role": "assistant", "content": agent_response_json})

        sentence = Sentence(
            sentence=agent_response_json['sentence'],
            words=generate_words(agent_response_json['sentence'])
        )

        return sentence

    
def generate_words(sentence: str) -> list[Word]:

    # Agregamos espacios antes y después de cada signo de puntuación
    sentence_with_spaces = re.sub("([.,!?;])", r' \1 ', sentence)

    elements = sentence_with_spaces.split()

    # Creamos una lista de diccionarios, donde cada diccionario representa un elemento
    # y tiene un indicador de si es una palabra (no un signo de puntuación).
    elements_with_indicators = [
        {'word': element, 'is_word': element not in string.punctuation}
        for element in elements
    ]

    # Aquí seleccionamos aleatoriamente palabras para preguntar al usuario.
    words = [elemento for elemento in elements_with_indicators if elemento['is_word']]
    num_words_to_ask = max(1, len(words) // 5)

    question_indexes = random.sample(range(len(words)), num_words_to_ask)
    
    # Agregamos el indicador de pregunta a los elementos que son palabras.
    for i, element in enumerate(elements_with_indicators):
        if element['is_word']:
            element['askable'] = i in question_indexes
        else:
            element['askable'] = False

    return [Word(**element) for element in elements_with_indicators]
