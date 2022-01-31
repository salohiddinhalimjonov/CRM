from django.contrib import admin
from .models import TimeUnit, Speciality, Advertisement, Teacher, Course, OnlyContacted, Student, AttendedMockLesson

admin.site.register([TimeUnit, Speciality, Advertisement, Teacher, Course,OnlyContacted, Student, AttendedMockLesson])