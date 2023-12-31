from django.urls import path
from .views import *

urlpatterns = [
    path('create_course', create_course, name='create_course'),
    path('add_course_photo/<int:courseid>', add_course_photo, name='add_course_photo'),
    path('get_all_course', get_all_course, name='get_all_course'),
    path('get_course_by_id/<int:courseid>', get_course_by_id, name='get_course_by_id'),
    path('update_course/<int:courseid>', update_course, name='update_course'),
    path('delete_course/<int:courseid>', delete_course, name='delete_course'),
    path('create_section', create_section, name='create_section'),
    path('get_course_section/<int:courseid>', get_course_section, name='get_course_section'),
    path('update_section/<int:courseid>/<int:sectionid>', update_section, name='update_section'),
    path('delete_section/<int:sectionid>', delete_section, name='delete_course'),
    path('create_sub_section', create_sub_section, name='create_sub_section'),
    path('get_sub_section_on_section/<int:sectionid>', get_sub_section_on_section, name='get_sub_section_on_section'), 
    path('get_sub_section_on_course/<int:courseid>', get_sub_section_on_course, name='get_sub_section_on_course'),
    path('delete_sub_section/<int:subsectionid>', delete_sub_section, name='delete_sub_section'),
    path('assign_course', assign_course, name='assign_course'),
    path('get_courses_by_user/<str:useremail>', get_courses_by_user, name='get_courses_by_user'),
    path('get_user_by_course/<int:courseid>', get_user_by_course, name='get_user_by_course'),
    path('create_category', create_category, name='create_category'),
    path('get_all_categories', get_all_categories, name='get_all_categories'),
    path('add_rating_course', add_rating_course, name='add_rating_course'),
    path('get_all_user_rating/<int:courseid>', get_all_user_rating, name='get_all_user_rating'),
    path('get_course_rating/<int:courseid', get_course_rating, name='get_course_rating'),
]
    