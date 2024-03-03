import pytest
from django.contrib.auth.models import User,Group
from rest_framework.test import APIClient
from api.models import *
@pytest.fixture
def client():
    return APIClient()
@pytest.fixture
def group():
    group=Group.objects.create( name='chef')
    return group
@pytest.fixture
def group_worker():
    group_worker=Group.objects.create( name='worker')
    return group_worker

@pytest.fixture
def user():
    user=User.objects.create_user(
        password='azert1234',
        first_name='test',
        last_name='test',
        email='test@gmail.com',
        username='test@gmail.com'
        
    )
    return user
@pytest.fixture
def user_2():
    user_2=User.objects.create_user(
        first_name='test2',
        last_name='test2',
        email='test2@gmail.com',
        password='azert123',
        username='test2@gmail.com'
        
    )
    return user_2

@pytest.fixture
def company():
    company=Company.objects.create(
        name_company='test_company'
    )
    return company

@pytest.fixture
def service():
    service=Service.objects.create( 
            name_service='mon_service',
            type_treatment='withtime',
            time_treatment=15,
            waiting_time=5     
                     
                     )
    return service
@pytest.fixture
def service_2():
    service_2=Service.objects.create( 
            name_service='mon_service_2',
            type_treatment='withtime',
            time_treatment=20,
            waiting_time=7     
                     )
    return service_2
@pytest.fixture
def programme():
    programme=Programme.objects.create(
        day='sunday',
        start_time='08:00:00',
        end_time='16:00:00'
         )
    return programme
@pytest.fixture
def programme_2():
    programme_2=Programme.objects.create(
        day='friday',
        start_time='08:00:00',
        end_time='16:00:00'
         )
    return programme_2
@pytest.fixture
def break_time():
    break_time=Break_time.objects.create(
        start_time_break='12:00:00',
        end_time_break='12:30:00'
         )
    return break_time
@pytest.fixture
def break_time_2():
    break_time_2=Break_time.objects.create(
        start_time_break='09:00:00',
        end_time_break='09:30:00'
         )
    return break_time_2
from django.conf import settings

