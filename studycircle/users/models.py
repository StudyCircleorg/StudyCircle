from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    major = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)