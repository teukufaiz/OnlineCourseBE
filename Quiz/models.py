from django.db import models
from Course.models import *

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_title = models.CharField(max_length=100)
    quiz_section_origin = models.ForeignKey(Section, on_delete=models.CASCADE)
    quiz_course_origin = models.ForeignKey(Course, on_delete=models.CASCADE)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    question_img = models.CharField(max_length=150)
    question_origin = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    answer_question_origin = models.ForeignKey(Question, on_delete=models.CASCADE)