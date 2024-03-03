import pytest
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from user.models import *
from unittest.mock import patch
from django.conf import settings
from datetime import datetime , timedelta
@pytest.mark.django_db       
class Test_user:
    def test_create_user(self,client):
        paylead=dict(
        password='azert123',
        first_name='test',
        last_name='test',
        email='test@gmail.com'            
        )
        response=client.post('/api/user/',data=paylead,format='json')
        assert response.status_code==201
    def test_update_password(self,client,user):
        paylead=dict(
            old_password='azert1234',
            new_password='daniel123',
            new_password_conf='daniel123'
        )
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response=client.put('/api/user/password/update/',data=paylead, format='json')
        assert response.status_code==200
    def test_forget_password(self,user,client):
        with patch('user.views.send_mail') as mock_send_mail:
            email=user.email
            response=client.post('/api/user/forgetpassword', data={'email':email},format='json')
            assert response.status_code==200
            code=PasswordCode.objects.get(user=user)
            mock_send_mail.assert_called_once_with(
                 'Password renitialisation',
                f'Your code of password renitialisation : {code.code}',
                [email],
                  )
            code=PasswordCode.objects.get(user=user)
            assert code.code!=None
    def test_ressetpassword(self,client,user):
        PasswordCode.objects.create(
            user=user,
            code='12345',
            time_expire=datetime.now() + timedelta(minutes=60)
        )
        payload=dict(
            email=user.email,
            code='12345',
            new_password='azert123'
        )
        response=client.post('/api/user/resetpassword',data=payload,format='json')
        assert response.status_code==200