from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, ActivationSerializer, LoginSerializer

'''
1. Регистрация
2. Активация
3. Логин
4. Восстановаление пароля
5. Смена пароля
6. Профиль пользователяв
'''

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('ваш аккаунт успешно зарегстрирован',status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('ваш аккаунт успешно активирован', status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    pass

class ResetPasswordView(APIView):
    pass

class ChangePasswordView(APIView):
    pass

class UserProfile(APIView):
    pass