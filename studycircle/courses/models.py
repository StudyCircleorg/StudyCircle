from django.db import models

# Create your models here.
class Course(models.Model):
    department = models.CharField(max_length=50)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.department} {self.level}"