from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.listening import Listening, SentenceCheckRequest, SentenceCheckResult
from open_ai.listening_planner import save_listening, generate_sentence, recover_listening_sentence, update_listening
from open_ai.topic_planner import get_random_topic

from users.auth import get_current_user

router = APIRouter(prefix='/listenings', tags=["listenings"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(get_current_user)])

@router.post('/', response_model=Listening, status_code=status.HTTP_200_OK)
def create_listening(num_sentences: int):
     try:
        random_topic = get_random_topic()
        listening = Listening(topic=random_topic)
        listening = save_listening(listening)
        sentences = [{}]*num_sentences
        for num_sentence in range(num_sentences):
            sentences[num_sentence] = generate_sentence(num_sentence, random_topic)
        listening.sentences = sentences
        update_listening(listening.id, sentences)
        return listening
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating context")

@router.post('/{listening_id}/sentences/{sentence_id}/check', response_model=SentenceCheckResult, status_code=status.HTTP_200_OK)
def check(listening_id: str, sentence_id: str, sentence_check_request: SentenceCheckRequest):
    answer_correct, correct_sentence = answer_is_correct(listening_id, sentence_id, sentence_check_request)
    if answer_correct:
        return SentenceCheckResult(correct=True, correct_sentence=correct_sentence)
    else:
        return SentenceCheckResult(correct=False, correct_sentence=correct_sentence)
    
def answer_is_correct(listening_id: str, sentence_id: str, sentence_check_request: SentenceCheckRequest) -> Tuple[bool, str]:
    listening_sentence = recover_listening_sentence(listening_id, sentence_id)
    return sentence_check_request.user_sentence.lower() == listening_sentence.correct_sentence.lower(), listening_sentence.correct_sentence
