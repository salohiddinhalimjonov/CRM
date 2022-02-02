from rest_framework import serializers
from .models import Holiday, DateTimeOfEntering, DateTimeOfExiting
from users.serializers import UserProfileSerializer
from students.serializers import TimeUnitSerializer


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model=Holiday
        fields=('education_centre', 'holiday_name', 'holiday_date', 'holiday_duration', 'time_unit')


class DateTimeOfEnteringSerializer(serializers.ModelSerializer):
    class Meta:
        model=DateTimeOfEntering
        fields='__all__'


class DateTimeOfExitingSerializer(serializers.ModelSerializer):
    class Meta:
        model=DateTimeOfExiting
        fields='__all__'
