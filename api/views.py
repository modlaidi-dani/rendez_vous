from django.shortcuts import render
from .models import * 
from .serializers import * 
from .permissions import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import response,status
import datetime
class ProfileViewset(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    authentication_classes=[TokenAuthentication]  
    def get_permissions(self):
        if self.action in ['update','delate','partial_update']:
            return [IsAuthenticated(),IsUser()]
        return [IsAuthenticated()]
     
    def get_queryset(self):
        user=self.request.user
        profile=user.profile
        company=profile.company
        queryset=super().get_queryset()
        if self.action in ['list','retrieve']:
            queryset=queryset.filter(company=company)
            return queryset
        else:
            return queryset   
    def create(self, request, *args, **kwargs):
        return Response ({"Error":"The creation is not aurorised"},status=status.HTTP_405_METHOD_NOT_ALLOWED)   
class CompanyViewset(viewsets.ModelViewSet):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    authentication_classes=[TokenAuthentication]  
    def get_permissions(self):
        if self.action in ['update','delate','partial_update']:
            return [IsAuthenticated(),IsChef(),UserInCompany()]
        if self.action in ['create']:
            return [IsAuthenticated(),IsChef()]
        return [AllowAny()]
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            company=serializer.save()
            profile=Profile.objects.filter(user=request.user).first()
            if profile.company is None:
                profile.company=company
                profile.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else: 
                return Response({'message':'You alredy have a compny'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ServiceViewset(viewsets.ModelViewSet):
    queryset=Service.objects.all()
    serializer_class=ServiceSerializer
    authentication_classes=[TokenAuthentication]  
    def get_permissions(self):
        if self.action in ['create','update','delate','partial_update']:
            return [IsAuthenticated(),IsChef(),UserInCompany_service()]
        return [AllowAny()]
    def create(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"message": "Profile not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        company=profile.company
        request.data['company']=company.id
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            Service=serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProfileService(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsChef,WorkerInCompany]
    
    def partial_update(self, request, *args, **kwargs):
        for index in request.data.keys():
            if index!='service':
                
                return Response({'Error': 'You cant update auther fields then Service'}, status=status.HTTP_400_BAD_REQUEST)          
        service_id = request.data.get('service')
        if service_id is None:  
            return Response({'error': 'Service ID is required'}, status=status.HTTP_400_BAD_REQUEST)
       
        instance = self.get_object()
        profile=Profile.objects.get(user=request.user)
        services=profile.company.services.all()
        try:
            service = Service.objects.get(id=service_id)
            if not service in services:
                return Response({'error': 'The Company have not this Service'}, status=status.HTTP_400_BAD_REQUEST)    
            instance.service=service
            instance.save()            
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:           
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
    def create(self, request, *args, **kwargs):
        return Response (status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        return Response (status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        return Response (status=status.HTTP_405_METHOD_NOT_ALLOWED)
class ProgrammeViewset(viewsets.ModelViewSet):
    queryset=Programme.objects.all()
    serializer_class=ProgrammeSerializer
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsAuthenticated(),UserInService_InCompany_Programme()]
        if self.action=='create':
            return [IsAuthenticated()]
        return [AllowAny()]
    def create(self, request, *args, **kwargs):
        day=request.data.get('day')
        profile=Profile.objects.get(user=request.user)
        service=profile.service
        if Programme.objects.filter(day=day, service=service).exists():
            return Response({'Error': f'Your programme on {day} already exists'}, status=status.HTTP_400_BAD_REQUEST)

        start_time=request.data.get('start_time')
        end_time=request.data.get('end_time')
        try:
            programme=Programme.objects.get(day=day,start_time=start_time,end_time=end_time)
            service=Service.objects.get(id=service.id)
            service.programmes.add(programme)
            service.save()
            serializer=self.get_serializer(programme)
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        except Programme.DoesNotExist:
            
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer) 
                programme = serializer.instance  
                service = Service.objects.get(id=service.id)
                service.programmes.add(programme)  
                service.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        profile=Profile.objects.get(user=request.user)
        service_user=profile.service
        if service_user in instance.service.all():
            instance.service.remove(service_user)

        if len(instance.service.all()) == 0:
            instance.delete()
        else:
            instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    def  update(self, request, *args, **kwargs):
        instance = self.get_object()
        request_day=request.data.get('day')
        profile=Profile.objects.get(user=request.user)
        service_user=profile.service
        other_services_count = instance.service.exclude(id=service_user.id).count()
        if request_day==instance.day:
            if other_services_count > 0:
                instance.service.remove(service_user)
                instance.save()
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        else:
            return Response({'Errore':'The day is note the same '}, status=status.HTTP_400_BAD_REQUEST)
            
class BreakViewset(viewsets.ModelViewSet):
    queryset=Break_time.objects.all()
    serializer_class=BreakTimeSerializer
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsAuthenticated(),BreakInService()]
        if self.action=='create':
            return [IsAuthenticated()]
        return [AllowAny()]
    def create(self, request, *args, **kwargs):
        start_time_break=request.data.get('start_time_break')
        end_time_break=request.data.get('end_time_break')
        start_time_break = datetime.datetime.strptime(start_time_break, '%H:%M:%S').time()
        end_time_break = datetime.datetime.strptime(end_time_break, '%H:%M:%S').time()
        day_request=request.data.get('day')
        profile=Profile.objects.get(user=request.user)
        programmes=profile.service.programmes.all()
        if day_request=='all':
            for prog in programmes:
                if (start_time_break < prog.start_time or end_time_break > prog.end_time):
                    return Response({'Error': 'Your break time is out of work time'}, status=status.HTTP_400_BAD_REQUEST)                
                else:
                    breaks = prog.breaks_time.filter(start_time_break__gt=start_time_break, 
                                  start_time_break__lt=end_time_break,
                                  end_time_break__gt=start_time_break,
                                  end_time_break__lt=end_time_break)
                    if breaks.exists():
                        return Response({'Error': f'A break at the same time already exists in {prog.day}'},status=status.HTTP_400_BAD_REQUEST)
                    try:
                        breaks=Break_time.objects.get(start_time_break=start_time_break,end_time_break=end_time_break)
                        prog.breaks_time.add(breaks)
                        profile.service.breaks_time.add(breaks)
                    except Break_time.DoesNotExist:
                        break_time = Break_time.objects.create(start_time_break=start_time_break, end_time_break=end_time_break)
                        prog.breaks_time.add(break_time)
                        profile.service.breaks_time.add(break_time)
                        
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
               self.perform_create(serializer)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        elif(day_request=='sunday' or day_request=='monday'or day_request=='tuesday'or day_request=='wednesday' or day_request=='thursday' or day_request=='friday'or day_request=='saturday'):
            prog=programmes.get(day=day_request)
            if (start_time_break < prog.start_time or end_time_break > prog.end_time):
                return Response({'Error': 'Your break time is out of work time'}, status=status.HTTP_400_BAD_REQUEST)                
            else:
                breaks = prog.breaks_time.filter(start_time_break__gt=start_time_break, 
                                  start_time_break__lt=end_time_break,
                                  end_time_break__gt=start_time_break,
                                  end_time_break__lt=end_time_break)
                if breaks.exists():
                    return Response({'Error': 'A break at the same time already exists'},status=status.HTTP_400_BAD_REQUEST)
                breaks=Break_time.objects.filter(start_time_break=start_time_break,end_time_break=end_time_break)
                if breaks.exists():
                    prog.breaks_time.add(breaks[0])
                    profile.service.breaks_time.add(breaks[0])
                    serializer=self.get_serializer(breaks[0])
                    return Response(serializer.data,status=status.HTTP_201_CREATED) 
                else:
                    serializer=self.get_serializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save() 
                        breaks = serializer.instance  
                        prog.breaks_time.add(breaks)  
                        profile.service.breaks_time.add(breaks)
                        return Response(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Invalid day request'}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        day_request=request.data.get('day')
        profile=Profile.objects.get(user=request.user)
        programmes=profile.service.programmes.all()
        if day_request=='all':
            for prog in programmes:
                if instance in prog.breaks_time.all():
                    prog.breaks_time.remove(instance)                
                    profile.service.breaks_time.remove(instance)
            if len(instance.programmes.all())==0:
                instance.delete()
            return Response ({'Message':'Delete succsefuly'},status=status.HTTP_204_NO_CONTENT)
        elif(day_request=='sunday' or day_request=='monday'or day_request=='tuesday'or day_request=='wednesday' or day_request=='thursday' or day_request=='friday'or day_request=='saturday'):
            try:
                prog=programmes.get(day=day_request)
                if instance in prog.breaks_time.all():
                        prog.breaks_time.remove(instance)                
                        profile.service.breaks_time.remove(instance)
                else:
                    return Response ({'Error':'The break dosent exists'},status= status.HTTP_400_BAD_REQUEST)
                if len(instance.programmes.all())==0:
                    instance.delete()
                return Response ({'Message':'Delete succsefuly'},status=status.HTTP_204_NO_CONTENT)
            except Programme.DoesNotExist:
                return Response({'Error': 'Your programme dosent exists'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'Error': 'Invalid day request'}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        day_request=request.data.get('day')
        start_time_break=request.data.get('start_time_break')
        end_time_break=request.data.get('end_time_break')
        start_time_break = datetime.datetime.strptime(start_time_break, '%H:%M:%S').time()
        end_time_break = datetime.datetime.strptime(end_time_break, '%H:%M:%S').time()
        profile=Profile.objects.get(user=request.user)
        programmes=profile.service.programmes.all()
        if day_request=='all':
            auther_services= instance.services.exclude(id=profile.service.id)
            if not auther_services:
                for prog in programmes:
                    if instance in prog.breaks_time.all():
                        if start_time_break < prog.start_time or end_time_break > prog.end_time:
                            return Response({'Error': 'Your break time is out of work time'}, status=status.HTTP_400_BAD_REQUEST)                
                        breaks = prog.breaks_time.filter(start_time_break__gt=start_time_break, 
                                    start_time_break__lt=end_time_break,
                                    end_time_break__gt=start_time_break,
                                    end_time_break__lt=end_time_break)
                        if breaks.exists() and len(breaks)>=2:                            return Response({'Error': f'A break at the same time already exists in {prog.day}'},status=status.HTTP_400_BAD_REQUEST)
                serializer=self.get_serializer(instance,data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                for prog in programmes:
                    if instance in prog.breaks_time.all():

                        if (start_time_break < prog.start_time or end_time_break > prog.end_time):
                            return Response({'Error': 'Your break time is out of work time'}, status=status.HTTP_400_BAD_REQUEST)                
    
                        breaks = prog.breaks_time.filter(start_time_break__gt=start_time_break, 
                                    start_time_break__lt=end_time_break,
                                    end_time_break__gt=start_time_break,
                                    end_time_break__lt=end_time_break)
                        if breaks.exists() and len(breaks)>=2:
                            return Response({'Error': f'A break at the same time already exists in {prog.day}'},status=status.HTTP_400_BAD_REQUEST)
                        prog.breaks_time.remove(instance)
                        profile.service.breaks_time.remove(instance)
                        if request.data.get('start_time_break'):
                            request.data['end_time_break']=instance.end_time_break
                        elif request.data.get('end_time_break'):
                            request.data['start_time_break']=instance.start_time_break                        
                        serializer=self.get_serializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        break_instance = serializer.instance  
                        prog.breaks_time.add(break_instance)
                        profile.service.breaks_time.add(break_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif(day_request=='sunday' or day_request=='monday'or day_request=='tuesday'or day_request=='wednesday' or day_request=='thursday' or day_request=='friday'or day_request=='saturday'):
            prog=programmes.get(day=day_request)
            if instance in prog.breaks_time.all():
                if start_time_break < prog.start_time or end_time_break > prog.end_time:
                    return Response({'Error': 'Your break time is out of work time'}, status=status.HTTP_400_BAD_REQUEST)                
        
                breaks = prog.breaks_time.filter(start_time_break__gt=start_time_break, 
                                start_time_break__lt=end_time_break,
                                end_time_break__gt=start_time_break,
                                end_time_break__lt=end_time_break)
                if breaks.exists() and len(breaks)>=2:
                    return Response({'Error': f'A break at the same time already exists in {prog.day}'},status=status.HTTP_400_BAD_REQUEST)
                if len(instance.programmes.all())==1:
                    serializer=self.get_serializer(instance,data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                prog.breaks_time.remove(instance)
                profile.service.breaks_time.remove(instance)
                if request.data.get('start_time_break'):
                    request.data['end_time_break']=instance.end_time_break
                elif request.data.get('end_time_break'):
                    request.data['start_time_break']=instance.start_time_break                        
                serializer=self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                break_instance = serializer.instance  
                prog.breaks_time.add(break_instance)
                profile.service.breaks_time.add(break_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)    
        else:
            return Response({'Error': 'Invalid day request'}, status=status.HTTP_400_BAD_REQUEST)
