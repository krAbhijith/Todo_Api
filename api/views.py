from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from api.models import Todo
from api.serializers import TodoSerializers, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User

import jwt, datetime





class RegisterApi(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response('user created successfully')
        else:
            return Response('user creation failed')
        
class LoginApi(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        user = User.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class LogoutApi(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "you successfullu logged out"
        }       
        return response


class TodoOperations(APIView):

    def get_user_id(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user_id = payload['id']
        user = User.objects.filter(id=user_id).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        return(user_id)
    
    def get(self, request):
        user_id = self.get_user_id(request)
        todos = Todo.objects.filter(user=user_id)
        serializer = TodoSerializers(todos, many = True)
        return Response(serializer.data)
    

    def post(self, request):
        todo = request.data
        user_id = self.get_user_id(request)
        todo["user"] = user_id
        serializer = TodoSerializers(data = todo)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)
        

    def put(self, request):
        pk = request.data['id']
        user_id = self.get_user_id(request)
        todo = get_object_or_404(Todo, pk = pk, user=user_id)
        serializer = TodoSerializers(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

    def patch(self, request):
        pk = self.request.data['id']
        user_id = self.get_user_id(request)
        todo = get_object_or_404(Todo, pk = pk, user=user_id)
        serializer = TodoSerializers(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)
        

    def delete(self, request):
        pk = request.data['id']
        user_id = self.get_user_id(request)
        get_object_or_404(Todo, pk=pk, user=user_id).delete()
        return Response('Deleted todo successfully')
    

        
        

