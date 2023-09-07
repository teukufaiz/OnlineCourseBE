from django.urls import path
from .views import *

urlpatterns = [
    path('create_quiz', create_quiz, name='create_quiz'),
    path('get_quiz_by_id/<int:quizid>', get_quiz_by_id, name='get_quiz_by_id'),
    path('update_quiz/<int:quizid>', update_quiz, name='update_quiz'),
    path('delete_quiz/<int:quizid>', delete_quiz, name='delete_quiz'),
    path('create_question/<int:quizid>', create_question, name='create_question'),
    path('get_question_on_quiz/<int:quizid>', get_question_on_quiz, name='get_question_on_quiz'),
    path('update_question/<int:quizid>/<int:questionid>', update_question, name='update_question'),
    path('delete_question/<int:questionid>', delete_question, name='delete_question'),
    path('create_answer/<int:questionid>', create_answer, name='create_answer'),
    path('get_answer_on_question/<int:questionid>', get_answer_on_question, name='get_answer_on_question'),
    path('update_answer/<int:questionid>/<int:answerid>', update_answer, name='update_answer'),
    path('delete_answer/<int:answerid>', delete_answer, name='delete_answer'),
]