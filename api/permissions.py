from rest_framework.permissions import BasePermission
from .models import * 
from django.contrib.auth.models import User,Group

class UserInCompany(BasePermission):
    def has_object_permission(self, request, view, obj):
        profile=Profile.objects.get(user=request.user)
        company=profile.company
        return obj==company        
class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):      
        return obj.user==request.user
class IsChef(BasePermission):
    def has_permission(self, request, view):      
        profile=Profile.objects.get(user=request.user)
        group=profile.groupe
        if group.name=='chef':
            return True
        elif group.name=='worker':
            return False
class UserInCompany_service(BasePermission):
    def has_object_permission(self, request, view, obj):      
        obj=obj.company
        IsIncompany=UserInCompany.has_object_permission(self,request,view,obj)
        return IsIncompany
class WorkerInCompany(BasePermission):
    def has_object_permission(self, request, view, obj):
        profile=Profile.objects.get(user=request.user)
        company=profile.company
        if obj.groupe.name=='worker':
            return obj.company==company
        else: 
            return False
class UserInService_InCompany_Programme(BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user=request.user)
        services_instance = obj.service.all()
        for service in services_instance:
            if service.company == profile.company and service.id==profile.service.id:
                return True
        return False
class BreakInService(BasePermission):
    def has_object_permission(self,request,view,obj):
        obj_programmes=obj.programmes.all()
        obj_services=obj.services.all()
        profile = Profile.objects.get(user=request.user)
        service=profile.service
        service_programmes=service.programmes.all()
        if set(obj_programmes) & set(service_programmes) and service in obj_services:
            return True
        else:
            return False