import base64
import time
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.chat import Activity, ActivityType, AgentAnalysis, AgentFlashCardActivity, MessageContentType, MessageType, ServerContext, ServerMessage, UserMessage
from open_ai.activity_planner import recover_activity_messages_db
from open_ai.analyst import analyze_message
from open_ai.flashcard_activity_planner import create_flashcard_activity
from open_ai.general import check_conversation_exists
from open_ai.talker import answer_message, start_conversation

from elevenlabs.speaker import text_to_speech
from open_ai.transcriptor import transcribe
import os

from users.auth import get_current_user

router = APIRouter(prefix='/chat', tags=["chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=ServerContext, status_code=status.HTTP_200_OK)
def create_context(user_message: UserMessage):
     try:
        context_id, chatgpt_response = start_conversation(user_message.content)
        return ServerContext(context_id=context_id, content=chatgpt_response)
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating context")


@router.post('/{context_id}', response_model=list[ServerMessage], status_code=status.HTTP_200_OK)
def chat(context_id: str, response_type: MessageContentType, user_message: UserMessage):
    if user_message.content_type == MessageContentType.TEXT:
        if response_type == MessageContentType.AUDIO:
            return chat_text_audio(context_id, user_message)
        return chat_text_text(context_id, user_message)
    elif user_message.content_type == MessageContentType.AUDIO:
        if response_type == MessageContentType.AUDIO:
            return chat_audio_audio(context_id, user_message)
        return chat_audio_text(context_id, user_message)

def chat_text_text(context_id: str, user_message: UserMessage) -> list[ServerMessage]:
    return analyze_message_and_generate_response(context_id, user_message.content, MessageContentType.TEXT)

def chat_text_audio(context_id: str, user_message: UserMessage) -> list[ServerMessage]:
     try:
        return analyze_message_and_generate_response(context_id, user_message.content, MessageContentType.AUDIO)
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")
    
def chat_audio_text(context_id: str, user_message: UserMessage) -> list[ServerMessage]:
    NANOts = time.time_ns() # generate to avoid clobber
    audio_filename = f"user_{NANOts}.mp3"
    audio_bytes = base64_to_bytes(user_message.content)
    try:
        with open(f'{audio_filename}', 'wb') as buffer:
            #shutil.copyfileobj(audio_bytes, buffer)
            buffer.write(audio_bytes)
            transcription = transcribe(audio_filename)
            print(transcription)
            return analyze_message_and_generate_response(context_id, transcription, MessageContentType.TEXT)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error loading audio")
    finally:
        delete_file(audio_filename)

def chat_audio_audio(context_id: str, user_message: UserMessage) -> list[ServerMessage]:
    NANOts = time.time_ns() # generate to avoid clobber
    audio_filename = f"user_{NANOts}.mp3"
    audio_bytes = base64_to_bytes(user_message.content)
    try:
        with open(f'{audio_filename}', 'wb') as buffer:
            #shutil.copyfileobj(audio_bytes, buffer)
            buffer.write(audio_bytes)
            transcription = transcribe(audio_filename)
            print(transcription)
            return analyze_message_and_generate_response(context_id, transcription, MessageContentType.AUDIO)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error loading audio")
    finally:
        delete_file(audio_filename)

def analyze_message_and_generate_response(context_id: str, user_message: str, response_type: MessageContentType) -> list[ServerMessage]:
    agent_analysis = analyze_message(context_id, user_message)
    if exist_analysis_errors(agent_analysis):

        if exist_grammatical_error(agent_analysis) or exist_spelling_error(agent_analysis):
            activity_type = generate_random_activity()
            if activity_type == ActivityType.FLASHCARD:
                flashcard_activity = create_flashcard_activity(context_id, agent_analysis)
                server_messages = []
                activity_introduction_message = get_activity_introduction_message(agent_analysis, flashcard_activity)

                server_messages.append(
                    generate_conversation_message_based_on_response_type(activity_introduction_message, response_type)
                )

                server_messages.append(
                    ServerMessage(
                        content_type=MessageContentType.TEXT,
                        message_type=MessageType.ACTIVITY, 
                        content=flashcard_activity
                    )
                )
                return server_messages
        
        #elif exist_pronunciation_error(agent_analysis):

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Activity {activity_type.value} is not available yet.")

    else:
        return [generate_conversation_message_based_on_response_type(talker_response(context_id, user_message), response_type)]

def generate_conversation_message_based_on_response_type(server_message: str, response_type: MessageContentType) -> ServerMessage:
    if response_type == MessageContentType.TEXT:
        return ServerMessage(
                    content_type=MessageContentType.TEXT,
                    message_type=MessageType.CONVERSATION, 
                    content=server_message
                )
    try:
        audio_bytes = text_to_speech(server_message)
        audio_data_base64 = bytes_to_base64(audio_bytes)
        return ServerMessage(
                        content_type=MessageContentType.AUDIO,
                        message_type=MessageType.CONVERSATION, 
                        content=audio_data_base64
                    )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")
    
def talker_response(context_id: str, user_message: str) -> str:
    try:
        return answer_message(context_id, user_message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating response")
        
def answer_is_correct(context_id: str, activity_type: ActivityType, user_message: str) -> bool:
    check_conversation_exists(context_id)
    activity_messages_db = recover_activity_messages_db(context_id, activity_type)
    if len(activity_messages_db) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is no {activity_type.value} activity.")
    
    # Switch between different activities (better to have some dictionary or whatever to avoid conditions)
    if activity_type == ActivityType.FLASHCARD:
        last_activity_db = activity_messages_db[-1]
        flashcard_activity = AgentFlashCardActivity(**last_activity_db['message']['content'])
        return user_message == flashcard_activity.flascard.correct_sentence, flashcard_activity.flascard.correct_sentence
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Activity {activity_type.value} is not available yet.")

def base64_to_bytes(base64Text: str):
    try:
        audio_bytes = base64.b64decode(base64Text)
        return audio_bytes
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 data") from e
     
def bytes_to_base64(audio_bytes):
    encoded_string = base64.b64encode(audio_bytes).decode('utf-8')
    return encoded_string    

def delete_file(filename: str):
     if os.path.isfile(filename):
        os.remove(filename)

def exist_analysis_errors(agent_analysis: AgentAnalysis):
    return (len(agent_analysis.grammatical_errors) > 0) or \
        (len(agent_analysis.spelling_errors) > 0) or \
        (len(agent_analysis.pronunciation_errors) > 0)

def exist_grammatical_error(agent_analysis: AgentAnalysis):
    return len(agent_analysis.grammatical_errors) > 0

def exist_spelling_error(agent_analysis: AgentAnalysis):
    return len(agent_analysis.spelling_errors) > 0

def exist_pronunciation_error(agent_analysis: AgentAnalysis):
    return len(agent_analysis.pronunciation_errors) > 0

def generate_random_activity():
    activity_type = ActivityType.FLASHCARD # TODO choose random activity
    return activity_type

def get_activity_introduction_message(agent_analysis: AgentAnalysis, activity: Activity):
    activity_intro_message = ""
    if len(agent_analysis.grammatical_errors) > 0:
        activity_intro_message = f"Oops, there's a gramatical error in the sentence {activity.incorrect}.\n "\
                f"Here you have a {activity.activity_type} to practice."

    elif len(agent_analysis.spelling_errors) > 0:
        activity_intro_message = f"Oops, there's a spelling error in the sentence {activity.incorrect}.\n "\
                f"Here you have a {activity.activity_type} to practice."
        
    elif len(agent_analysis.pronunciation_errors) > 0:
        activity_intro_message=f"Oops, there's a pronunciation error in the sentence {activity.incorrect}.\n "\
                f"Here you have a {activity.activity_type} to practice."
        
    return activity_intro_message

@router.post('/{context_id}/activity', response_model=list[ServerMessage], status_code=status.HTTP_200_OK)
def answer_activity(context_id: str, message: UserMessage, activity_type: ActivityType | None = None):
    answer_correct, correct_sentence = answer_is_correct(context_id, activity_type, message.content)
    if answer_correct:
        return [
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=talker_response(context_id, message.content)
            )
        ]
    else:
        server_messages = []
        server_messages.append(
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=f"Oops.. that's not the right answer. The correct sentence would be: {correct_sentence}.\n"
            )
        )
        server_messages.append(
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=f"All right, let's continue!\n"
            )
        )
        server_messages.append(
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=talker_response(context_id, correct_sentence)
            )
        )
        return server_messages