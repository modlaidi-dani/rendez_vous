from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class DaysOfWeek(models.TextChoices):
    SUNDAY= 'sunday'
    MONDAY= 'monday'
    TUESDAY= 'tuesday'
    WEDNESDAY= 'wednesday'
    THURDAY= 'thursday'
    FRIDAY='friday'
    SATURDAY='saturday'   
class TypeTreatment(models.TextChoices):
    CLASSIC='classic'
    WITHTIME='withtime'
class Company(models.Model):
    name_company=models.CharField(max_length=100,null=False)

class Break_time(models.Model):
    start_time_break=models.TimeField( auto_now=False, auto_now_add=False,null=True)    
    end_time_break=models.TimeField( auto_now=False, auto_now_add=False,null=True)    
    
class Programme(models.Model):
    day=models.CharField(max_length=20,null=True ,choices=DaysOfWeek.choices)
    start_time=models.TimeField( auto_now=False, auto_now_add=False,null=True)    
    end_time=models.TimeField( auto_now=False, auto_now_add=False,null=True)    
    breaks_time=models.ManyToManyField(Break_time,related_name='programmes')
class Service (models.Model):
    name_service=models.CharField(max_length=100,null=False)
    company=models.ForeignKey(Company,null=True ,on_delete=models.CASCADE,related_name='services')
    max_treatment=models.IntegerField(null=True,default=1)
    type_treatment=models.CharField(max_length=20,null=True ,choices=TypeTreatment.choices)
    time_treatment=models.IntegerField(null=True,default=10)
    waiting_time=models.IntegerField(null=True,default=5)
    programmes=models.ManyToManyField(Programme,related_name='service')
    breaks_time=models.ManyToManyField(Break_time,related_name='services')
    
class Profile(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.SET_NULL,related_name='profile')  
    first_name=models.CharField(max_length=100,null=False)
    last_name=models.CharField(max_length=100,null=False)
    email=models.EmailField( max_length=254,null=False)
    company=models.ForeignKey(Company,null=True ,on_delete=models.CASCADE)
    groupe=models.ForeignKey(Group,null=True, on_delete=models.CASCADE)
    service=models.ForeignKey(Service,null=True, on_delete=models.SET_NULL)

@receiver(post_save, sender=User)
def save_profile(sender,instance,created, **kwargs):
    user= instance
    if created:
        Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
        

    
