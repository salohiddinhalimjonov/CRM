from django.contrib import admin
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student,Penalty

admin.site.register([TimeUnit, Advertisement,Penalty, Teacher, Course,OnlyContacted, Student])