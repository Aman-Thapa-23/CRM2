from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class UserProfile(models.Model): 
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

#we don't need agent first name and last name because we already have it in Abstractuser. 
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)

#There can be many leads and each lead have agent. It is for the record of the personal info who we need to get
# in contact And it is not neccessary that lead is going to logged in into teh system. So we need name in this model  
class Lead(models.Model):       
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

