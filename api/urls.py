from django.urls import path,include
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register('programme',ProgrammeViewset)
router.register('profile',ProfileViewset)
router.register('company',CompanyViewset)
router.register('service',ServiceViewset,basename='service')
router.register('break_time',BreakViewset)
router.register('patch_profile_service',ProfileService)


urlpatterns = [
    path('',include(router.urls)),
]