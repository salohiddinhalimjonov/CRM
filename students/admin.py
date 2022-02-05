from django.contrib import admin
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student

admin.site.register([TimeUnit, Advertisement, Teacher, Course,OnlyContacted, Student])