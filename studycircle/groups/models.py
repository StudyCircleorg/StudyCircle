import datetime
from django.db import models

from courses.models import Course
from users.models import User

# Define choices for session types
SESSION_TYPE_CHOICES = [
    ('exam_review', 'Exam Review'),
    ('collab_learning', 'Collaborative Learning'),
    ('quiet_study', 'Quiet Study'),
    ('discussion_debate', 'Discussion and Debate'),
]

# Define choices for group dynamics
GROUP_DYNAMICS_CHOICES = [
    ('social', 'Social'),
    ('intensive', 'Intensive Study'),
    ('mixed', 'Mixed (Study + Breaks)'),
    ('flexible', 'Flexible'),
]

LOCATION_CHOICES = [
    ('rutherford', 'Rutherford'),
    ('sperber', 'Sperber'),
    ('cameron', 'Cameron'),
]

class Group(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(verbose_name="Group Bio", blank=True)
    meeting_date = models.DateField(verbose_name="Meeting Date", default=datetime.date.today)
    meeting_time = models.TimeField(verbose_name="Meeting Time", default=datetime.time(12, 0))
    session_type = models.CharField(max_length=100, choices=SESSION_TYPE_CHOICES)
    dynamics = models.CharField(max_length=100, choices=GROUP_DYNAMICS_CHOICES)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)

    def __str__(self):
        return self.name
    
class GroupCourse(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)