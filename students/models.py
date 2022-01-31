from django.db import models
from uuid import uuid4
import os
from django.conf import settings
import uuid


def image_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('thumb/',filename)


class TimeUnit(models.Model):  #example : day, month, year
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    date_added = models.DateField()


class Speciality(models.Model): #related to Teacher
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)


class Teacher(models.Model):
    education_centre = models.ManyToManyField(settings.AUTH_USER_MODEL)
    full_name = models.CharField(max_length=128)
    passport_id = models.CharField(max_length=16)
    photo = models.ImageField(upload_to=image_path, null=True,blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    speciality = models.ManyToManyField(Speciality)
    experience = models.IntegerField()
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.PROTECT)
    date_of_receipt = models.DateField(auto_now_add=True)



class Course(models.Model):
    education_centre = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=32)
    duration = models.IntegerField()
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    date_started = models.DateField()
    teacher = models.ManyToManyField(Teacher)
    number_of_groups = models.IntegerField()


class OnlyContacted(models.Model): #Students who are interested in this education centre and contacted for getting info about it
    education_centre = models.ManyToManyField(settings.AUTH_USER_MODEL)
    full_name = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    phone_number = models.CharField(max_length=16)
    course_interested = models.ManyToManyField(Course)
    date_of_contacting = models.DateField(auto_now_add=True)
    advertisement = models.ManyToManyField(Advertisement)


class Student(models.Model): #Contacted students who decided to be a student of the education centre
    student_id = models.CharField(max_length=100,unique=True, default=uuid.uuid4)# default id is also generated for this model,
    # but every student should have their unique id that it gives a chance for a student to study in different education centres using
    # this crm system at the same time
    only_contacted = models.OneToOneField(OnlyContacted, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_path, null=True, blank=True)
    parent_phone_number = models.CharField(max_length=16)
    selected_course = models.ManyToManyField(Course)
    has_paid_fee = models.BooleanField(default=False)
    date_of_receipt = models.DateField(auto_now_add=True)


class AttendedMockLesson(models.Model):#contacted students who attended in mock lessons to determine whether they study in the education centre or not
    onlyContacted = models.ManyToManyField(OnlyContacted)
    lesson_attended = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    date_of_attending = models.DateField(auto_now_add=True)

