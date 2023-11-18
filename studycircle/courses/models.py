from django.db import models

# Create your models here.
class Course(models.Model):
    department = models.CharField(max_length=50)
    level = models.IntegerField()