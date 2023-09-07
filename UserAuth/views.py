import json
import jwt
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from Jwt.views import MyTokenObtainPairView
from .models import *

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        hash_password = make_password(deserialize['password'])
        if User.objects.filter(email=deserialize['email']).exists():
            return JsonResponse({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        elif deserialize['password'] != deserialize['verif_password']:
            return JsonResponse({'message': 'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User(name=deserialize['name'], email=deserialize['email'], password=hash_password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        deserialize = json.loads(request.body)
        email = deserialize['email']
        password = deserialize['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            tokens = MyTokenObtainPairView.as_view()(request).data
            return JsonResponse(tokens)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            refresh_token = data.get('refresh_token', '')

            if refresh_token:
                try:
                    refresh_token_obj = RefreshToken(refresh_token)
                    refresh_token_obj.blacklist()
                    logout(request)
                    return JsonResponse({'message': 'Logout success'}, status=status.HTTP_200_OK)
                except Exception as e:
                    return JsonResponse({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)