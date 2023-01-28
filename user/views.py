from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.decorators import api_view

@api_view(['PATCH'])
def reset_password(request):
    data = request.data
    user = User.objects.get(pk= request.user.id)
    if (user.check_password(data['currentPassword'])):
        user.set_password(data["newPassword"])
        user.save()
        return Response({"message":"Password Changed successfully"},status=200)
    else:
        return Response({"message":"Invalid current password. Please enter your current password."},status=400)




class UserViewset(APIView):
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'PATCH':
            return [permissions.IsAuthenticated(),]
        return super().get_permissions()



    def get(self,request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def patch(self,request):
        user = User.objects.get(pk=request.user.id)
        data = request.data
        serializer = UserSerializer(instance=user,data=data)
        if (request.user.email != data['email'] or request.user.username != data["username"]):
            try:
                User.objects.get(email = data["email"])
                return Response({"message":"A user with that email already exists."},status=400)
            except User.DoesNotExist:
                if (request.user.username != data["username"]):
                    try:
                        User.objects.get(username = data["username"])
                        return Response({"message":"A user with that username already exists"},status=400)
                    except User.DoesNotExist:
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data)
                        else:
                            return Response(serializer.errors,status=400)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
    def post(self,request):
        data = request.data
        try:
            User.objects.get(username = data["username"])
            return Response({"message":"This username is not Available. Please change your username."},status=400)
        except User.DoesNotExist:
            try:
                User.objects.get(email = data["email"])
                return Response({"message":"This email address  is not available. Please change your email address."})
            except User.DoesNotExist:
                user = User(username=data["username"])
                user.set_password(data["password"])
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.email = data["email"]
                user.save()
                return Response({"message":"Sign up successful.Signing in and redirecting to home page."})