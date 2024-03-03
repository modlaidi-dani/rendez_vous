from django.shortcuts import render
from .serializers import * 
from .models import PasswordCode
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import status
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerialier
    authentication_classes=[TokenAuthentication]
    
    def get_permissions(self):
        if self.action in ['update','delate','partial_update']:
            return [IsAuthenticated()]
        return [AllowAny()]
class UpdateUserPassword(UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=SerializerUpdatePassword
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        user=request.user
        if not user.check_password(request.data.get('old_password')): 
            return Response ({'Error':'Password incorrect'},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response ({'Message':'Password changed succesfully'},status=status.HTTP_200_OK)
class ForgetPassword(generics.GenericAPIView):
    serializer_class=ForgetPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'] 
        try:
                user=User.objects.get(email=email)
                password_code,_=PasswordCode.objects.get_or_create(user=user)
                code=''.join([str(random.randint(0,9))for _ in range(5)])
                time_expire= datetime.now() + timedelta(minutes=60)
                password_code.time_expire=time_expire
                password_code.code=code
                send_mail(
                    'Password renitialisation',
                    f'Your code of password renitialisation : {code}',
                    [email],
                    
                )
                password_code.save()
                return Response ({"Message":f"The code was sended fro the email:{email}"},status=status.HTTP_200_OK)
        except User.DoesNotExist:
                return Response({'Error':'The email dosent existe'},status=status.HTTP_404_NOT_FOUND)
class ResetPassword(generics.GenericAPIView):
    def post(self, request): 
        code=request.data.get('code')
        try:
            password_code=PasswordCode.objects.get(code=code)
            if password_code.time_expire<datetime.now().date():
                return Response ({'Error':'The code time is expired, You should send another message for your email'},status=status.HTTP_408_REQUEST_TIMEOUT)
            user=password_code.user
            user.set_password(request.data.get('new_password'))
            user.save()
            password_code.delete()
            return Response({'Message':'Your password is renialisated succefully'},status=status.HTTP_200_OK)
        except PasswordCode.DoesNotExist:
            return Response({'Error':'Incorrect code'},status=status.HTTP_400_BAD_REQUEST)