from django.db import models

from courses.models import Course
from users.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    meeting_times = models.TextField()
    days = models.CharField(max_length=100)
    session_type = models.CharField(max_length=100)
    dynamics = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    qr_code = models.URLField()

    def __str__(self):
        return self.name
    
class GroupCourse(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)