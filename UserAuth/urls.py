from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
    path('is_registered', is_registered, name='is_registered'),
    path('is_admin', is_admin, name='is_admin'),
]