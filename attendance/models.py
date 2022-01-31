from django.db import models
from students.models import Student, TimeUnit
from django.conf import settings

class Holiday(models.Model):   #holiday days are entered here. As a result these days are not added to absent days of students
    education_centre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    holiday_name = models.CharField(max_length=64)
    holiday_date = models.DateField()
    holiday_duration = models.IntegerField(default=1)
    time_unit = models.ForeignKey(TimeUnit, on_delete=models.PROTECT)


class DateTimeOfEntering(models.Model):  #date time of entering the education centre
    student = models.ForeignKey(Student, on_delete=models.CASCADE)#several students can not enter at the same time, but a student can enter in different time
    #Many(Date) to One(Student)
    datetime_of_entering = models.DateTimeField(auto_now_add=True)


class DateTimeOfExiting(models.Model):  #date time of exiting the education centre
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time_of_exiting = models.DateTimeField(auto_now_add=True)

