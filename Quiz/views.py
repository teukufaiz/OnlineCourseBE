import json
from .models import *
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_quiz (request):
    deserialize = json.loads(request.body)
    course = Course.objects.get(course_id=deserialize['courseid'])
    section = Section.objects.get(section_id=deserialize['sectionid'])
    quiz = Quiz(quiz_title=deserialize['title'], quiz_desc=deserialize['desc'], quiz_course_origin=course, quiz_section_origin = section)
    quiz.save()
    return JsonResponse({'message': 'Quiz created successfully'}, status=status.HTTP_201_CREATED)

def get_quiz_by_id (request, quizid):
    quiz = Quiz.objects.get(quiz_id = quizid)
    quiz_data = {
        'quiz_title': quiz.quiz_title
    }
    return JsonResponse({'Quiz': quiz_data}, safe=False, status=status.HTTP_200_OK)

def update_quiz (request, quizid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        quiz = Quiz.objects.get(quiz_id = quizid)

        new_title = deserialize['title']

        if new_title:
            quiz.quiz_title = new_title

        quiz.save()
        return JsonResponse({'message': 'Quiz updated successfully'}, status=status.HTTP_200_OK)

def delete_quiz (request, quizid):
    quiz = Quiz.objects.get(quiz_id = quizid)
    quiz.delete()
    return JsonResponse({'message': 'Quiz deleted successfully'}, status=status.HTTP_200_OK)

def create_question (request, quizid):
    deserialize = json.loads(request.body)
    quiz = Quiz.objects.get(quiz_id=quizid)
    question = Question(question_text=deserialize['question'], question_img=deserialize['img'], question_origin=quiz)
    question.save()
    return JsonResponse({'message': 'Question created successfully'}, status=status.HTTP_201_CREATED)

def get_question_on_quiz (request, quizid):
    quiz = Quiz.objects.get(quiz_id = quizid)
    questions = Question.objects.filter(question_origin = quiz)

    question_dict = {}
    for question in questions:
        question_data = {
            'question_text': question.question_text,
            'question_img': question.question_img
        }
        question_dict[question.question_id] = question_data
    
    return JsonResponse({'questions': question_dict}, safe=False, status=status.HTTP_200_OK)

def update_question (request, quizid, questionid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        quiz = Quiz.objects.get(quiz_id = quizid)
        question = Question.objects.get(question_id = questionid, question_origin = quiz)

        new_question = deserialize['question']
        new_img = deserialize['img']

        if new_question:
            question.question_text = new_question
        if new_img:
            question.question_img = new_img

        question.save()
        return JsonResponse({'message': 'Question updated successfully'}, status=status.HTTP_200_OK)
    
def delete_question (request, questionid):
    question = Question.objects.get(question_id = questionid)
    question.delete()
    return JsonResponse({'message': 'Question deleted successfully'}, status=status.HTTP_200_OK)

def create_answer (request, questionid):
    deserialize = json.loads(request.body)
    question = Question.objects.get(question_id=questionid)
    answer = Answer(answer_text=deserialize['answer'], is_correct=deserialize['correct'], answer_question_origin=question)
    answer.save()
    return JsonResponse({'message': 'Answer created successfully'}, status=status.HTTP_201_CREATED)

def get_answer_on_question (request, questionid):
    question = Question.objects.get(question_id = questionid)
    answers = Answer.objects.filter(answer_question_origin = question)

    answer_dict = {}
    for answer in answers:
        answer_data = {
            'answer_text': answer.answer_text,
            'is_correct': answer.is_correct
        }
        answer_dict[answer.answer_id] = answer_data
    
    return JsonResponse({'answers': answer_dict}, safe=False, status=status.HTTP_200_OK)

def update_answer (request, questionid, answerid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        question = Question.objects.get(question_id = questionid)
        answer = Answer.objects.get(answer_id = answerid, answer_question_origin = question)

        new_answer = deserialize['answer']
        new_correct = deserialize['correct']

        if new_answer:
            answer.answer_text = new_answer
        if new_correct:
            answer.is_correct = new_correct

        answer.save()
        return JsonResponse({'message': 'Answer updated successfully'}, status=status.HTTP_200_OK)


def delete_answer (request, answerid):
    answer = Answer.objects.get(answer_id = answerid)
    answer.delete()
    return JsonResponse({'message': 'Answer deleted successfully'}, status=status.HTTP_200_OK)