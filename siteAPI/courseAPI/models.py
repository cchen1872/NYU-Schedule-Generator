from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20, default='')
    subject = models.CharField(max_length = 10)
    school = models.CharField(max_length=5)
    # semester = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    courses = models.CharField(max_length=100)
    username = models.CharField(max_length=20)