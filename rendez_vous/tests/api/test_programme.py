import pytest
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.models import *

@pytest.mark.django_db       
class Test_programme:
    def test_create_add_new_programme(self,client,user,company,service):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        paylead=dict(
                day='sunday',
            start_time='08:00:00',
            end_time='16:00:00',
                    )
        
        response=client.post('/api/programme/',data=paylead,format='json')
        service=Service.objects.get(id=service.id)
        
        assert response.status_code==201
        assert response.data['id'] == service.programmes.all()[0].id


    def test_create_alredy_exste(self,client,user,company,service):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        programme=Programme.objects.create(
        day='sunday',
        start_time='08:00:00',
        end_time='16:00:00',
        )

        service.company=company
        service.programmes.add(programme)
        service.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
               day='sunday',
            start_time='08:00:00',
            end_time='16:00:00',
        )
        response=client.post('/api/programme/',data=paylead,format='json')
        assert response.status_code==400
    def test_create_add_programme_for_service(self,programme,client,user,company,service,service_2):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()

        service_2.company=company
        service_2.programmes.add(programme)
        service_2.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        paylead=dict(
               day='sunday',
            start_time='08:00:00',
            end_time='16:00:00',
        )
        service_1=Service.objects.get(id=service.id)
        service_2=Service.objects.get(id=service_2.id)
        response=client.post('/api/programme/',data=paylead,format='json')
        assert response.status_code==201
        assert programme in service_1.programmes.all()
        assert programme in service_2.programmes.all()
    def test_liste_programmes(self,client,company,programme,service):
        service.company=company
        service.programmes.add(programme)
        service.save()
        response=client.get('/api/programme/')
        assert response.status_code==200        
    def test_retrieve_programmes(self,client,company,programme,service):
        service.company=company
        service.programmes.add(programme)
        service.save()
        response=client.get(f'/api/programme/{programme.id}/')
        assert response.status_code==200
    def test_delete_programme_one_service(self,programme,client,service,company,user):    
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        service.company=company
        service.programmes.add(programme)
        service.save()
        response=client.delete(f'/api/programme/{programme.id}/')
        assert response.status_code==204
    def test_delete_programme_many_services(self,programme,client,service,service_2,company,user):    
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        service.company=company
        service.programmes.add(programme)
        service.save()
        service_2.company=company
        service_2.programmes.add(programme)
        service_2.save()
        response=client.delete(f'/api/programme/{programme.id}/')
        assert response.status_code==204
        assert programme.service.all()[0].id==service_2.id
    def test_update_authers_serices_existe(self,programme,client,service,service_2,company,user):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        service.company=company
        service.programmes.add(programme)
        service.save()
        service_2.company=company
        service_2.programmes.add(programme)
        service_2.save()
        paylead=dict(
               day='sunday',
            start_time='10:00:00',
            end_time='16:00:00',
        )        
        response=client.put(f'/api/programme/{programme.id}/',data=paylead,format='json')
        programmes=Programme.objects.all()
        assert response.status_code==200
        assert response.data['id']!=programme.id
        assert len(programmes)==2
    def test_update_one_serices_existe(self,programme,client,service,company,user):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        service.company=company
        service.programmes.add(programme)
        service.save()
        paylead=dict(
               day='sunday',
            start_time='10:00:00',
            end_time='16:00:00',
        )        
        response=client.put(f'/api/programme/{programme.id}/',data=paylead,format='json')
        programmes=Programme.objects.all()
        assert response.status_code==200
        assert response.data['id']==programme.id
        assert len(programmes)==1
    def test_permisssion_other_service(self,programme,client,service,service_2,company,user):
        profil=Profile.objects.get(user=user)
        profil.company=company
        profil.service=service_2
        profil.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        service.company=company
        service.programmes.add(programme)
        service.save()

        response=client.delete(f'/api/programme/{programme.id}/')
        assert response.status_code==403
        programmes=Programme.objects.all()
        assert programmes[0].id==programme.id
