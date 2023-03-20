from django.contrib import admin
from .models import Course, Schedule

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'school', 'username')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'courses', 'username')

admin.site.register(Course, CourseAdmin)
admin.site.register(Schedule, ScheduleAdmin)