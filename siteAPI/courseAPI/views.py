from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CourseSerializer, ScheduleSerializer
from .models import Course, Schedule

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    model = Course
    # queryset = 
    queryset = Course.objects.all().order_by('username')
    serializer_class = CourseSerializer
    def get_queryset(self):
        queryset = self.queryset
        curr_username = self.request.query_params.get('username')
        if curr_username is not None:
            queryset = queryset.filter(username=curr_username)
        return queryset


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer
    
    