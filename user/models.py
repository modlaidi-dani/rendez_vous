from django.db import models
from django.contrib.auth.models import User

class PasswordCode(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    code=models.IntegerField(null=True,unique=True)
    time_expire=models.DateField( null=True,auto_now=False, auto_now_add=False)

