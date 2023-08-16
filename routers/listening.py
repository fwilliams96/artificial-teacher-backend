from fastapi import APIRouter, Depends, HTTPException, status
from ai_teacher.activities.listening.application.listening_creator import ListeningCreator
from ai_teacher.activities.listening.application.listening_generator import ListeningGenerator
from ai_teacher.activities.listening.application.sentence_finder import SentenceFinder
from ai_teacher.activities.listening.application.topic_planner import TopicPlanner
from ai_teacher.activities.listening.domain.listening import Sentence
from ai_teacher.users.shared.application.user_auth import UserAuth
from ai_teacher.users.shared.domain.user import User
from db.models.listening import Listening, SentenceCheckResult

router = APIRouter(prefix='/listenings', tags=["listenings"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}}, dependencies=[Depends(UserAuth().get_current_user)])

@router.post('/', response_model=Listening, status_code=status.HTTP_200_OK)
def create_listening(num_sentences: int, user: User = Depends(UserAuth().get_current_user)):
     try:
        random_topic = TopicPlanner().user_random_topic(user.id)
        listening = ListeningGenerator().generate(random_topic, num_sentences)
        ListeningCreator().save(listening)
        return listening
     except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating context")

@router.post('/{listening_id}/sentences/{sentence_id}/check', response_model=SentenceCheckResult, status_code=status.HTTP_200_OK)
def check(listening_id: str, sentence_id: str, user_sentence: Sentence):
    sentence = SentenceFinder().find(listening_id=listening_id, sentence_id=sentence_id)
    sentence_is_correct = sentence.sentence.lower() == user_sentence.sentence.lower()
    if sentence_is_correct:
        return SentenceCheckResult(correct=True, correct_sentence=sentence.sentence)
    else:
        return SentenceCheckResult(correct=False, correct_sentence=sentence.sentence)