from django.urls import path,include
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register('',UserViewset)

urlpatterns = [
    path('',include(router.urls)),
    path('password/update/',UpdateUserPassword.as_view()),
    path('forgetpassword',ForgetPassword.as_view()),
    path('resetpassword',ResetPassword.as_view()),
    

]