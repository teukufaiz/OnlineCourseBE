import json

from Quiz.models import Quiz
from .models import *
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_course(request):
    deserialize = json.loads(request.body)
    course = Course(course_name=deserialize['name'], course_desc=deserialize['desc'], course_photo=deserialize['photo'], course_price=deserialize['price'])
    course.save()
    return JsonResponse({'message': 'Course created successfully'}, status=status.HTTP_201_CREATED)

def get_all_course(requests):
    courses = Course.objects.all()

    course_dict = {}
    for course in courses:
        course_data = {
            'course_id': course.course_id,
            'course_desc': course.course_desc,
            'course_photo': course.course_photo,
            'course_price': course.course_price,
            'course_created': course.course_created.strftime('%Y-%m-%d %H:%M:%S')
        }
        course_dict[course.course_name] = course_data

    return JsonResponse(course_dict, safe=False, status=status.HTTP_200_OK)

def get_course_by_id(request,courseid):
    course = Course.objects.filter(course_id=courseid).values("course_id","course_name","course_desc","course_photo","course_price","course_created")[0]
    return JsonResponse({"response":course}, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def assign_course(request):
    deserialize = json.loads(request.body)
    user = User.objects.get(email=deserialize['email'])
    course = Course.objects.get(course_id=deserialize['courseid'])
    course.enrolled_users.add(user)
    return JsonResponse({"message": "User assigned to course successfully"}, status=status.HTTP_200_OK)

def get_courses_by_user(request, useremail):
    user = User.objects.get(email=useremail)
    courses = list(user.enrolled_courses.all().values("course_id","course_name"))
    return JsonResponse({"response":courses}, safe=False, status=status.HTTP_200_OK)

def get_user_by_course(request, courseid):
    course = Course.objects.get(course_id=courseid)
    users = list(course.enrolled_users.all().values("email"))
    return JsonResponse({"response":users}, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def update_course(request,courseid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        course = Course.objects.get(course_id = courseid)
        new_name = deserialize['name']
        new_desc = deserialize['desc']
        new_price = deserialize['price']

        if new_name:
            course.course_name = new_name
        if new_desc:
            course.course_desc = new_desc
        if new_price:
            course.course_price = new_price

        course.save()

        return JsonResponse({"message": "Course updated successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def delete_course(request, courseid):
    course = Course.objects.get(course_id = courseid)
    course.delete()
    return JsonResponse({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def create_section(request):
    deserialize = json.loads(request.body)
    course = Course.objects.get(course_id=deserialize['courseid'])
    section = Section(section_name=deserialize['name'], section_course_origin=course)
    section.save()
    return JsonResponse({'message': 'Section created successfully'}, status=status.HTTP_201_CREATED)

def get_course_section(request,courseid):
    course = Course.objects.get(course_id = courseid)
    sections = Section.objects.filter(section_course_origin = course)

    section_dict = {}
    for section in sections:
        section_data = {
            'section_name': section.section_name,
        }
        section_dict[section.section_id] = section_data
    
    return JsonResponse({'sections': section_dict}, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def update_section(request,courseid,sectionid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        course = Course.objects.get(course_id = courseid)
        section = Section.objects.get(section_id = sectionid, section_course_origin = course)
        new_name = deserialize['name']

        section.section_name = new_name
        section.save()

        return JsonResponse({"message": "Section updated successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def delete_section(request, sectionid):
    section = Section.objects.get(section_id = sectionid)
    section.delete()
    return JsonResponse({"message": "Section deleted successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def create_sub_section(request):
    deserialize = json.loads(request.body)
    course = Course.objects.get(course_id=deserialize['courseid'])
    section = Section.objects.get(section_id=deserialize['sectionid'])
    subsection = SubSection(sub_section_title=deserialize['title'], sub_section_desc=deserialize['desc'], sub_section_video=deserialize['video'], sub_section_course_origin=course, sub_section_origin = section)
    subsection.save()
    return JsonResponse({'message': 'Sub section created successfully'}, status=status.HTTP_201_CREATED)

def get_sub_section_on_section (request, sectionid):
    section = Section.objects.get(section_id = sectionid)
    subsections = SubSection.objects.filter( sub_section_origin = section)

    subsection_dict = {}
    for subsection in subsections:
        subsection_data = {
            'sub_section_title': subsection.sub_section_title,
            'sub_section_desc': subsection.sub_section_desc,
            'sub_section_video': subsection.sub_section_video
        }
        subsection_dict[subsection.sub_section_id] = subsection_data

    return JsonResponse({'Sub section': subsection_dict}, safe=False, status=status.HTTP_200_OK)

def get_sub_section_on_course (request, courseid):
    course = Course.objects.get(course_id = courseid)
    subsections = SubSection.objects.filter( sub_section_course_origin = course)

    subsection_dict = {}
    for subsection in subsections:
        subsection_data = {
            'sub_section_title': subsection.sub_section_title,
            'sub_section_desc': subsection.sub_section_desc,
            'sub_section_video': subsection.sub_section_video
        }
        subsection_dict[subsection.sub_section_id] = subsection_data

    return JsonResponse({'Sub section': subsection_dict}, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def update_sub_section(request,subsectionid,courseid,sectionid):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        course = Course.objects.get(course_id = courseid)
        section = Section.objects.get(section_id = sectionid)
        subsection = SubSection.objects.get(sub_section_id = subsectionid, sub_section_course_origin = course, sub_section_origin = section)

        new_title = deserialize['title']
        new_desc = deserialize['desc']
        new_video = deserialize['video']

        if new_title:
            subsection.sub_section_title = new_title
        if new_desc:
            subsection.sub_section_desc = new_desc
        if new_video:
            subsection.sub_section_video = new_video

        subsection.save()

        return JsonResponse({"message": "Sub Section updated successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def delete_sub_section(request, subsectionid):
    subsection = SubSection.objects.get(sub_section_id = subsectionid)
    subsection.delete()
    return JsonResponse({"message": "Sub section deleted successfully"}, status=status.HTTP_200_OK)

def get_course_all_information(request, courseid):
    course = Course.objects.get(course_id=courseid)
    sections = Section.objects.filter(section_course_origin=course)

    course_structure = {}

    for section in sections:
        section_info = {}
        
        subsections = SubSection.objects.filter(sub_section_origin=section)
        section_subsections = {}
        
        for subsection in subsections:
            subsection_info = {'title': subsection.sub_section_title}
            section_subsections[subsection.sub_section_id] = subsection_info
        
        quizzes = Quiz.objects.filter(quiz_section_origin=section)
        section_quizzes = {}
        
        for quiz in quizzes:
            quiz_info = {'title': quiz.quiz_title}
            section_quizzes[quiz.quiz_id] = quiz_info
        
        section_info['subsections'] = section_subsections
        section_info['quizzes'] = section_quizzes
        
        course_structure[section.section_name] = section_info
        
    return JsonResponse(course_structure, safe=False, status=status.HTTP_200_OK)