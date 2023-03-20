# serializers.py
from rest_framework import serializers

from .models import Course, Schedule

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'subject', 'school', 'username')

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'courses', 'username')
