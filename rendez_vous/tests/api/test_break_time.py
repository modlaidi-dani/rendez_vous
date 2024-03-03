import pytest
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.models import *

@pytest.mark.django_db       
class Test_break_time:
    def test_create_new_breaktime_one_day(self, client,user,programme,service):
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        service.programmes.add(programme)
        service.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
            day='sunday',
            start_time_break='12:00:00',
            end_time_break='13:00:00'
        )
        response=client.post('/api/break_time/',data=paylead,format='json')
        break_time=programme.breaks_time.all()        
        assert response.status_code==201
        assert len(break_time)==1 
        assert response.data['id']==break_time[0].id
    def test_create_new_breaktime_all_day(self, client,user,programme,programme_2,service):
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        service.programmes.add(programme)
        service.programmes.add(programme_2)
        service.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
            day='all',
            start_time_break='12:00:00',
            end_time_break='13:00:00'
        )
        response=client.post('/api/break_time/',data=paylead,format='json')
        break_time=programme.breaks_time.all()        
        break_time_2=programme_2.breaks_time.all()
        assert response.status_code==201
        assert break_time[0].id==break_time_2[0].id
    def test_delete_breaktime_one_time(self, client,user,programme,break_time,service):
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        service.programmes.add(programme)
        service.breaks_time.add(break_time)
        programme.breaks_time.add(break_time)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        programme.breaks_time.add(break_time)
        paylead=dict(
            day='sunday'
        )
        response=client.delete(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        assert response.status_code==204
#1): one breaktime, one programme,one service
    def test_update_break_1(self,client,service,programme,break_time,user):
            
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        service.programmes.add(programme)
        service.breaks_time.add(break_time)
        programme.breaks_time.add(break_time)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
            day='sunday',
            start_time_break='11:00:00',
            end_time_break='13:00:00'
        )
        response=client.put(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        break_time=Break_time.objects.get(id=break_time.id)
        assert response.status_code==200
        assert response.data['id']==break_time.id        
        assert response.data['start_time_break']==str(break_time.start_time_break)        
    # out of programme time     
        paylead=dict(
            day='sunday',
            start_time_break='6:00:00',
            end_time_break='09:00:00'
        )
        response=client.put(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        assert response.status_code==400
        
#2): one breaktime,programmes=2,one service
    def test_update_break_2(self,client,service,programme_2 ,programme,break_time,user):
            
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        service.programmes.add(programme)
        service.programmes.add(programme_2)
        service.breaks_time.add(break_time)
        programme.breaks_time.add(break_time)
        programme_2.breaks_time.add(break_time)

        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
            day='all',
            start_time_break='09:00:00',
            end_time_break='10:00:00'
        )
        response=client.put(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        break_time=Break_time.objects.get(id=break_time.id)
        break_programme_1=programme.breaks_time.all()
        break_programme_2=programme_2.breaks_time.all()
        assert response.status_code==200
        assert response.data['id']==break_time.id
        assert response.data['id']==break_programme_1[0].id        
        assert response.data['id']==break_programme_2[0].id                        
        assert response.data['start_time_break']==str(break_time.start_time_break)        
        assert response.data['start_time_break']==str(break_programme_1[0].start_time_break)        
        assert response.data['start_time_break']==str(break_programme_2[0].start_time_break)        
    # out of programme time     
        paylead=dict(
            day='all',
            start_time_break='6:00:00',
            end_time_break='09:00:00'
        )
        response=client.put(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        assert response.status_code==400
        
#3): 2 breaktime, one programme,2 services
    def test_delate_break_2(self,client,service,service_2,programme,break_time,break_time_2,user,user_2):
            
        profil=Profile.objects.get(user=user)
        profil.service=service
        profil.save()
        profil_2=Profile.objects.get(user=user_2)
        profil_2.service=service_2
        profil_2.save()

        service.programmes.add(programme)
        service_2.programmes.add(programme)
        service.breaks_time.add(break_time)
        service_2.breaks_time.add(break_time_2)
        programme.breaks_time.add(break_time)
        programme.breaks_time.add(break_time_2)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
            day='sunday'
        )
        response=client.delete(f'/api/break_time/{break_time_2.id}/',data=paylead,format='json')
        assert response.status_code==403
        response=client.delete(f'/api/break_time/{break_time.id}/',data=paylead,format='json')
        assert response.status_code==204

        
        
        
        
        