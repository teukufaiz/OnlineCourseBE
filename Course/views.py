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
    course = Course(course_name=deserialize['name'], course_desc=deserialize['desc'], course_photo='', course_price=deserialize['price'])
    course.save()
    if (not deserialize['category']):
        if Category.objects.filter(category_name='uncategorized').exists():
            category = Category.objects.get(category_name='uncategorized')
            course.course_category.add(category)
        else:
            new_category = Category(category_name='uncategorized')
            new_category.save()
            course.course_category.add(new_category)
    else:
        for categoryid in deserialize['category']:
            category = Category.objects.get(category_id=categoryid)
            course.course_category.add(category)

    course_id = course.course_id

    return JsonResponse({'courseId': course_id}, status=status.HTTP_201_CREATED)

@csrf_exempt
def add_course_photo(request, courseid):
    deserialize = json.loads(request.body)
    course = Course.objects.get(course_id = courseid)
    course.course_photo = deserialize['photo']
    course.save()
    return JsonResponse({"message": "Course photo added successfully"}, status=status.HTTP_200_OK)

def get_all_course(requests):
    courses = Course.objects.all().order_by('course_name')

    course_list = []
    for course in courses:
        course_data = {
            'course_id': course.course_id,
            'course_name': course.course_name,
            'course_desc': course.course_desc,
            'course_rating' : course.course_rating,
            'course_photo': course.course_photo,
            'course_price': course.course_price,
            'course_created': course.course_created,
            'course_categories': [{'category_id': category.category_id, 'category_name': category.category_name} for category in course.course_category.all()]
        }
        course_list.append(course_data)

    return JsonResponse(course_list, safe=False, status=status.HTTP_200_OK)

def get_course_by_id(request,courseid):
    course = Course.objects.filter(course_id=courseid).first()
    course_data = {
        'course_id': course.course_id,
        'course_name': course.course_name,
        'course_desc': course.course_desc,
        'course_photo': course.course_photo,
        'course_rating' : course.course_rating,
        'course_price': course.course_price,
        'course_created': course.course_created,
        'course_categories': [{'category_id': category.category_id, 'category_name': category.category_name} for category in course.course_category.all()]
    }
    return JsonResponse({"response":course_data}, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
def create_category(request):
    deserialize = json.loads(request.body)
    category = Category(category_name=deserialize['newcategory'])
    category.save()
    return JsonResponse({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)

def get_all_categories(request):
    categories = Category.objects.all()
    category_list = [{'category_id': category.category_id, 'category_name': category.category_name} for category in categories]
    return JsonResponse({"response": category_list}, safe=False, status=status.HTTP_200_OK)

def add_rating_course(request):
    deserialize = json.loads(request.body)
    course = Course.objects.get(course_id=deserialize['courseid'])
    user = User.objects.get(email=deserialize['email'])
    new_rating = deserialize['rating']

    if course.rating_users:
        course.course_rating = (course.course_rating * len(course.rating_users.all()) + new_rating) / (len(course.rating_users.all()) + 1)
        course.rating_users.add(user)
        course.save()
    else:
        course.rating_users.add(user)
        course.course_rating = new_rating
        course.save()

    return JsonResponse({"message": "Rating added successfully"}, status=status.HTTP_200_OK)

def get_all_user_rating(request, courseid):
    course = Course.objects.get(course_id=courseid)
    users = course.rating_users.all()
    user_list = [{'email': user.email} for user in users]
    return JsonResponse({"response": user_list}, safe=False, status=status.HTTP_200_OK)

def get_course_rating(request, courseid):
    course = Course.objects.get(course_id=courseid)
    rating = course.course_rating
    return JsonResponse({"response": rating}, safe=False, status=status.HTTP_200_OK)

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
        new_photo = deserialize['photo']
        new_price = deserialize['price']
        
        if new_name:
            course.course_name = new_name
        if new_desc:
            course.course_desc = new_desc
        if new_photo:
            course.course_photo = new_photo
        if new_price:   
            course.course_price = new_price

        course.save()

        course.course_category.clear()

        if (not deserialize['category']):   
            category = Category.objects.get(category_name='uncategorized')
            course.course_category.add(category)
        else:
            for category_id in deserialize['category']:
                category = Category.objects.get(pk=category_id)
                course.course_category.add(category)

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