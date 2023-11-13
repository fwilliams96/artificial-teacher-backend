from openai import OpenAI
client = OpenAI()

from fastapi import HTTPException, status

def send_messages_to_ai(messages: list[dict], json_mode = False) -> str:
    try:
        if json_mode:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                response_format={"type": "json_object"},
                messages=messages
            )
        else:    
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages
            )
        response_content = response.choices[0].message.content
        ##print(f"Chatgpt choices: {response}")
        return response_content
    except Exception as e:
        #print(f"Exception calling chatgpt: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exception calling chatgpt")
    
def interpret_image(messages: list[dict]): 
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=300
    )
    #print(response.choices[0])
    return response.choices[0].message.content

def generate_image(prompt: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        #print(f"Exception calling chatgpt: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exception generating image with dall-e")

def transcribe_audio_to_text(audio_file) -> str:
    return client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )