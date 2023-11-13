from fastapi import HTTPException, status
from ai_teacher.analysis.grammar.domain.external_grammar_analyst import ExternalGrammarAnalyst
from ai_teacher.analysis.shared.domain.analysis import SentenceAnalysis, SentenceAnalysisType
from shared.infrastructure.openai.client.openai_client import send_messages_to_ai
from shared.infrastructure.utils.utils import check_is_valid_json_and_get_correct_json, string_to_json

class ChatgptGrammarAnalyst(ExternalGrammarAnalyst):

    json_format = {
        "grammatical_errors": ["list of grammatical errors"], 
        "comments": "your extra comments"
    }

    json_example_format = {
        "grammatical_errors": ["It's a future sentence, it should use 'I will play'"], 
        "comments": "N/A"
    }

    analyst_context = "You are an English grammar error analyst and your job is to analyze the sentences I will provide you. "\
    f"Identify only the grammatical errors and return them in the following JSON format: {json_format}."

    analyst_assistant = f"{string_to_json(json_example_format)}"

    analyst_user_message = lambda sentence: "Please analyze the following sentence: " + sentence

    def analyze(self, sentence: str) -> SentenceAnalysis:
        messages=[{"role": "system", "content": self.analyst_context}]
        messages.append({"role": "user", "content": ChatgptGrammarAnalyst.analyst_user_message("I play football tomorrow")})
        messages.append({"role": "assistant", "content": self.analyst_assistant})
        messages.append({"role": "user", "content": ChatgptGrammarAnalyst.analyst_user_message(sentence)})

        #print(f"\n>>>>>>>>>>>>>>>>> [GRAMMAR ANALYST] Sent messages <<<<<<<<<<<<<<<<<<<\n")
        #print(f"{messages} \n")
        agent_response = send_messages_to_ai(messages)
        #print(f"\n>>>>>>>>>>>>>>>>> [GRAMMAR ANALYST] Received message <<<<<<<<<<<<<<<<<<<\n")
        #print(f"{agent_response} \n")

        max_retries = 1
        retries = 0
        retry_messages = []
        retry_messages.extend(messages)
        valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
        while (not valid_json) and (retries < max_retries):
            #print(f"\n>>>>>>>>>>>>>>>>> [GRAMMAR ANALYST] Sent messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            #print(f"{retry_messages} \n")
            retry_messages.append({"role": "user", "content": "Return the response in the JSON format I asked you in the first message please."})
            agent_response = send_messages_to_ai(retry_messages)
            #print(f"\n>>>>>>>>>>>>>>>>> [GRAMMAR ANALYST] Received messages (retry) <<<<<<<<<<<<<<<<<<<\n")
            #print(f"{agent_response} \n")
            valid_json, agent_response = check_is_valid_json_and_get_correct_json(agent_response)
            retries += 1

        if retries == max_retries and not valid_json:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred generating the activity")

        agent_response_json = string_to_json(agent_response)
        messages.append({"role": "assistant", "content": agent_response_json})

        return SentenceAnalysis(
            type=SentenceAnalysisType.GRAMMAR,
            errors=agent_response_json['grammatical_errors'],
            comment=agent_response_json(agent_response_json['comment'])
        )