import datetime
from django.db import models

from groups.models import Group

from django.db import models
from django.utils import timezone

class Session(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)

    def is_upcoming(self):
        # Check if the session date and time are in the future
        now = timezone.now()
        session_datetime = timezone.make_aware(datetime.datetime.combine(self.date, self.start_time))
        return session_datetime > now