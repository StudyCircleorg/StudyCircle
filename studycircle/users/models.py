from django.db import models
from django.contrib.auth.models import AbstractUser

from studycircle.courses.models import Course

# Create your models here.
class User(AbstractUser):
    major = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)