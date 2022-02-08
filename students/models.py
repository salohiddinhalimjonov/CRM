from uuid import uuid4
import random
import string
import os
from django.db import models
from django.conf import settings

def image_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('thumb/',filename)

def generate_random_id():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    all = lower + upper + num
    random_id = random.sample(all, 10)
    string_id = "".join(random_id)
    return string_id

class TimeUnit(models.Model):  #example : day, month, year
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    date_added = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']


class Penalty(models.Model):
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    penalty_in_percent = models.FloatField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']


class Course(models.Model):
    UNIT = (
        ('So\'m', 'So\'m'),
        ('$','$')
    )
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    duration = models.IntegerField()
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    date_started = models.DateField()
    number_of_groups = models.IntegerField()
    cost_per_month = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.TextField(choices=UNIT,default='So\'m')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128)
    passport_id = models.CharField(max_length=16)
    photo = models.ImageField(upload_to=image_path, null=True,blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    course = models.ManyToManyField(Course)
    experience = models.IntegerField()
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.PROTECT)
    date_of_receipt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering=['experience']


class OnlyContacted(models.Model): #Students who are interested in this education centre and contacted for getting info about it
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128,null=True,blank=True)
    phone_number = models.CharField(max_length=16)
    course_interested = models.ManyToManyField(Course)
    date_of_contacting = models.DateField(auto_now_add=True)
    advertisement = models.ManyToManyField(Advertisement)
    has_been_student = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class Student(models.Model): #Contacted students who decided to be a student of the education centre
    UNIT = (
        ('So\'m', 'So\'m'),
        ('$', '$')
    )
    student_id = models.CharField(max_length=10,unique=True, default=generate_random_id)# default id is also generated for this model,
    # but every student should have their unique id, it is used for determining student attendance
    only_contacted = models.OneToOneField(OnlyContacted, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_path, null=True, blank=True)
    parent_phone_number = models.CharField(max_length=16)
    selected_course = models.ManyToManyField(Course)
    date_of_receipt = models.DateField(auto_now_add=True)
    has_paid_fee = models.BooleanField(default=False)
    date_of_last_payment = models.DateField()
    penalty = models.ManyToManyField(Penalty)
    total_payment_per_month = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit1 = models.TextField(choices=UNIT, default='So\'m')
    total_loan_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit2 = models.TextField(choices=UNIT, default='So\'m')

    def __str__(self):
        return self.student_id


