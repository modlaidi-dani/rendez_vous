import pytest
from datetime import time
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.models import *
@pytest.mark.django_db
class Test_profile:
    def test_liste_profile(slef,user,client):
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response=client.get(f'/api/profile/')
        assert response.status_code==200           
    def test_retrieve_profile(self,user,client):
        profil=Profile.objects.get(user=user)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response=client.get(f'/api/profile/{profil.id}/')
        assert response.data['user']==user.id
        assert response.status_code==200
    def test_create_profile(slef,user,client):
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        payload = {    'username':'test1'}
        response = client.post('/api/profile/', data=payload, format='json')
        assert response.status_code==405
    def test_update_profile(self,user,client):
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        profil=Profile.objects.get(user=user)
        payload=dict( 
            first_name='test',
            last_name='test'
                     )

        response=client.patch(f'/api/profile/{profil.id}/',data=payload, format='json')
        profil=Profile.objects.get(user=user)
        assert response.status_code==200
        assert response.data['first_name']==profil.first_name
        assert response.data['last_name']==profil.last_name
        assert response.data['email']==profil.email
    
@pytest.mark.django_db       
class Test_compay:
    def test_create_compny(self,group,user,client):
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.save()

        payload=dict( 
            name_company='ma_company'
                     )
            
        response = client.post('/api/company/', data=payload, format='json')
        profil=Profile.objects.get(user=user)
        
        assert response.status_code==201
        assert response.data['id']==profil.company.id
        assert response.data['name_company']==profil.company.name_company
        
    def test_list_company(self,client):
        response=client.get('/api/company/')
        assert response.status_code==200
        
    def test_retrieve_company(self,client,company):
        response=client.get(f'/api/company/{company.id}/')
        assert response.status_code==200
        
    def test_update_company(slef,client,user,company,group):
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        payload=dict( 
            name_company='ma_company'
                     )
            
        response = client.put(f'/api/company/{company.id}/', data=payload, format='json')
        company=Company.objects.get(id=company.id)
        assert response.status_code==200
        assert response.data['id']==company.id    
        assert response.data['name_company']==company.name_company    
    def test_delete_company(slef,client,user,company,group):
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete(f'/api/company/{company.id}/')
        assert response.status_code==204
@pytest.mark.django_db       
class Test_service:
    def test_create_service(self,client,user,group,company):
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        payload=dict( 
            name_service='mon_service',
            max_treatment=2,
            type_treatment='withtime',
            time_treatment=15,
            waiting_time=5     
                     )
            
        response = client.post('/api/service/', data=payload, format='json')
        assert response.status_code==201
        assert response.data['company']==company.id
        assert response.data['name_service']=='mon_service'
    def test_retrieve_service(self,client,service):
        response = client.get(f'/api/service/{service.id}/')
        assert response.status_code==200
    def test_liste_service(self,client):
        response = client.get('/api/service/')
        assert response.status_code==200
    
    def test_update_service(self,client,service,company,user,group):
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()
        service.company=company
        service.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        payload=dict( 
            name_service='new_name_service',
            max_treatment=2,
            type_treatment='classic',
            time_treatment=10,
            waiting_time=5     
                     )
        response = client.put(f'/api/service/{service.id}/',data=payload,format='json')
        service=Service.objects.get(id=service.id)
        assert response.status_code==200
        assert response.data['name_service']==service.name_service
        assert response.data['max_treatment']==service.max_treatment  
        assert response.data['type_treatment']==service.type_treatment
        assert response.data['time_treatment']==service.time_treatment
    def test_delate_service(self,client,service,company,user,group):
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()
        service.company=company
        service.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.delete(f'/api/service/{service.id}/')
        assert response.status_code==204
@pytest.mark.django_db       
class Test_worker_in_service:
    def test_worker_service(self,client,user,user_2,group,group_worker,company,service):
        service.company=company
        service.save()
        profil=Profile.objects.get(user=user)
        profil.groupe=group
        profil.company=company
        profil.save()

        profil_2=Profile.objects.get(user=user_2)
        profil_2.groupe=group_worker
        profil_2.company=company
        profil_2.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        payload=dict(
            service=service.id
        ) 
        
        response = client.patch(f'/api/patch_profile_service/{profil_2.id}/',data=payload,format='json')
        profil_2=Profile.objects.get(user=user_2)
        assert response.status_code==200
        assert response.data["service"]==profil_2.service.id
    