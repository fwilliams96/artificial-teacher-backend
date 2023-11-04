from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ai_teacher.chat.free.application.free_chat_agent_talker import FreeChatAgentTalker
from ai_teacher.chat.free.application.free_chat_finder import FreeChatFinder
from ai_teacher.chat.free.application.free_chat_finisher import FreeChatFinisher
from ai_teacher.chat.free.application.free_chat_generator import FreeChatGenerator
from ai_teacher.chat.free.domain.free_chat import FreeChat, FreeChatMessage
from ai_teacher.users.shared.application.user_auth import get_current_user
from ai_teacher.users.shared.application.user_score_incrementer import UserScoreIncrementer
from ai_teacher.users.shared.domain.user import UserDb

router = APIRouter(prefix='/free-chat', tags=["free-chat"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=FreeChat, status_code=status.HTTP_200_OK)
def create_chat(user: UserDb = Depends(get_current_user)):
     try:
        return FreeChatGenerator().create(user.id)
     except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating chat")

@router.post('/{chat_id}', response_model=list[FreeChatMessage], status_code=status.HTTP_200_OK)
def chat(chat_id: str, user_message: FreeChatMessage, response_in_speech: bool = False, user: UserDb = Depends(get_current_user)):
     try:
        user_message.chat_id = chat_id
        user_message.sender_id = user.id
        return FreeChatAgentTalker().talk(user_message, response_in_speech)
     except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating chat")
     
@router.get('/{chat_id}', response_model=FreeChat, status_code=status.HTTP_200_OK)
def recover_chat(chat_id: str):
   try:
      free_chat = FreeChatFinder().find(chat_id)
      if free_chat is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Free chat not found")
      return free_chat
   except Exception as e:
      #print(e)
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error recovering role play")
   
@router.post('/{chat_id}/finish', response_model=FreeChat, status_code=status.HTTP_200_OK)
def finish_chat(chat_id: str, background_tasks: BackgroundTasks, user: UserDb = Depends(get_current_user)):
     try:
        free_chat = FreeChatFinisher().finish(chat_id)
        background_tasks.add_task(UserScoreIncrementer().increment, user.id, 50)
        return free_chat
     except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error finishing chat")
     
'''
def answer_activity(context_id: str, response_type: MessageContentType, user_message: UserMessage) -> list[ServerMessage]:
    answer_correct, correct_sentence = answer_is_correct(context_id, user_message)
    if answer_correct:
        # TODO maybe we should not use the correct_sentence to continue the conversation and tell gpt to continue with another topic
        return answer_conversation(context_id, response_type, UserMessage(content=correct_sentence, content_type=MessageContentType.TEXT))
    else:
        server_messages = []
        server_messages.append(
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=f"Oops.. that's not the right answer. The correct sentence would be: <{correct_sentence}> .\n"
            )
        )
        server_messages.append(
            ServerMessage(
                content_type=MessageContentType.TEXT,
                message_type=MessageType.CONVERSATION, 
                content=f"All right, let's continue!\n"
            )
        )
        server_messages.extend(answer_conversation(context_id, response_type, user_message))
        return server_messages
    
def answer_conversation(context_id: str, response_type: MessageContentType, user_message: UserMessage) -> list[ServerMessage]:
    if user_message.content_type == MessageContentType.TEXT:
        if response_type == MessageContentType.AUDIO:
            return chat_text_audio(context_id, user_message.content)
        return chat_text_text(context_id, user_message.content)
    elif user_message.content_type == MessageContentType.AUDIO:
        if response_type == MessageContentType.AUDIO:
            return chat_audio_audio(context_id, user_message.content)
        return chat_audio_text(context_id, user_message.content)
    
def chat_text_text(context_id: str, user_message: str) -> list[ServerMessage]:
    return analyze_message_and_generate_response(context_id, user_message, MessageContentType.TEXT)

def chat_text_audio(context_id: str, user_message: str) -> list[ServerMessage]:
     try:
        return analyze_message_and_generate_response(context_id, user_message, MessageContentType.AUDIO)
     except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")
    
def chat_audio_text(context_id: str, user_message: str) -> list[ServerMessage]:
    NANOts = time.time_ns() # generate to avoid clobber
    audio_filename = f"user_{NANOts}.wav"
    audio_bytes = base64_to_bytes(user_message)
    try:
        with open(f'{audio_filename}', 'wb') as buffer:
            #shutil.copyfileobj(audio_bytes, buffer)
            buffer.write(audio_bytes)
            transcription = AudioToTextTranscriber().transcribe(audio_filename)
            return analyze_message_and_generate_response(context_id, transcription, MessageContentType.TEXT)
    except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error loading audio")
    finally:
        delete_file(audio_filename)

def chat_audio_audio(context_id: str, user_message: str) -> list[ServerMessage]:
    NANOts = time.time_ns() # generate to avoid clobber
    audio_filename = f"user_{NANOts}.wav"
    audio_bytes = base64_to_bytes(user_message)
    try:
        with open(f'{audio_filename}', 'wb') as buffer:
            #shutil.copyfileobj(audio_bytes, buffer)
            buffer.write(audio_bytes)
            transcription = AudioToTextTranscriber().transcribe(audio_filename)
            flashcard = get_server_response(context_id, transcription, MessageContentType.AUDIO)
            activity_introduction_message = get_activity_introduction_message(agent_analysis)

            return analyze_message_and_generate_response(context_id, transcription, MessageContentType.AUDIO)
    except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error loading audio")
    finally:
        delete_file(audio_filename)

def get_flashcard_server_response(sentence_analysis: SentenceAnalysis, response_type: MessageContentType) -> list[ServerMessage]:
        server_messages = []

        flashcard_introduction_message = generate_conversation_message_based_on_response_type(get_activity_introduction_message(sentence_analysis), response_type)
        server_messages.append(flashcard_introduction_message)

        flashcard = FlashcardGenerator().generate(sentence_analysis)
        server_messages.append(ServerMessage(
            content_type=MessageContentType.TEXT,
            message_type=MessageType.ACTIVITY, 
            content=flashcard
        ))
        return server_messages

def get_server_response(context_id: str, user_message: str, response_type: MessageContentType) -> list[ServerMessage]:
    grammar_sentence_analysis = GrammarAnalyst().analyze(user_message)

    if len(grammar_sentence_analysis.errors) > 0:
        return get_flashcard_server_response(grammar_sentence_analysis, response_type)

    spelling_sentence_analysis = SpellingAnalyst().analyze(user_message)
    if len(spelling_sentence_analysis) > 0:
        return get_flashcard_server_response(spelling_sentence_analysis, response_type)

    return [generate_conversation_message_based_on_response_type(talker_response(context_id, user_message), response_type)]

def generate_conversation_message_based_on_response_type(server_message: str, response_type: MessageContentType) -> ServerMessage:
    if response_type == MessageContentType.TEXT:
        return ServerMessage(
                    content_type=MessageContentType.TEXT,
                    message_type=MessageType.CONVERSATION, 
                    content=server_message
                )
    try:
        audio_data_base64 = TextToSpeechTransformer().transform_to_base64(server_message)
        return ServerMessage(
            content_type=MessageContentType.AUDIO,
            message_type=MessageType.CONVERSATION, 
            content=audio_data_base64
        )
    except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating audio")
    
def talker_response(context_id: str, user_message: str) -> str:
    try:
        return answer_message(context_id, user_message)
    except Exception as e:
        #print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating response")
        
def answer_is_correct(context_id: str, user_message: str) -> bool:
    check_conversation_exists(context_id)
    last_activity_message_db = recover_last_activity_message_db(context_id)
    if last_activity_message_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is no a current activity.")
    # Switch between different activities (better to have some dictionary or whatever to avoid conditions)
    activity_type = last_activity_message_db['message']['activity_type']
    if activity_type == ActivityType.FLASHCARD:
        flashcard_activity = AgentFlashCardActivity(**last_activity_message_db['message']['content'])
        #print(f"User option: {user_message}")
        #print(f"Correct option: {flashcard_activity.flashcard.correct_option}")
        #print(f"Match?: {user_message == flashcard_activity.flashcard.correct_option}")
        return user_message == flashcard_activity.flashcard.correct_option, flashcard_activity.flashcard.correct_sentence
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

def get_activity_introduction_message(sentence_analysis: SentenceAnalysis):
    activity_intro_message = f"Oops, there's a {sentence_analysis.type.value.lower()} error in the sentence.\n "\
        f"Here you have flashcard to practice."

    return activity_intro_message'''