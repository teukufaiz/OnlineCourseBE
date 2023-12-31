from django.db import models
from UserAuth.models import User

class Category(models.Model) :
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=30)
    course_desc = models.TextField(max_length=300)
    course_photo = models.CharField(max_length=150)
    course_price = models.IntegerField(default=0)
    course_rating = models.IntegerField(default=0)
    course_published = models.BooleanField(default=False)
    course_created = models.DateTimeField(auto_now_add=True)
    course_category = models.ManyToManyField(Category, related_name='courses')
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_courses')
    rating_users = models.ManyToManyField(User, related_name='rated_courses')

class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=30)
    section_course_origin = models.ForeignKey(Course, on_delete=models.CASCADE)

class SubSection(models.Model):
    sub_section_id = models.AutoField(primary_key=True)
    sub_section_title = models.CharField(max_length=30)
    sub_section_desc = models.TextField(max_length=300)
    sub_section_video = models.CharField(max_length=150)
    sub_section_course_origin = models.ForeignKey(Course, on_delete=models.CASCADE)
    sub_section_origin = models.ForeignKey(Section, on_delete=models.CASCADE)

