import openai

from fastapi import HTTPException, status

from shared.infrastructure.openai.client.config.openai_config import API_KEY

openai.api_key = API_KEY

def send_messages_to_ai(messages: list[dict]) -> str:
    try:
        response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        response_content = response.choices[0].message.content
        ##print(f"Chatgpt choices: {response}")
        return response_content
    except openai.error.RateLimitError:
        #print(f"Your user has exceed the quota")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Your user has exceed the quota")
    except Exception as e:
        #print(f"Exception calling chatgpt: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exception calling chatgpt")
    
def transcribe_audio_to_text(audio_file) -> str:
    response = openai.Audio.transcribe("whisper-1", audio_file)
    return response["text"]