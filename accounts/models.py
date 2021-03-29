from django.db import models
from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
from django import forms

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    address = models.CharField(max_length=30)
    mobile =  models.IntegerField()


    def __str__(self):
        return self.user.username
