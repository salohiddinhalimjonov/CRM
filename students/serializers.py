from rest_framework import serializers
from .models import TimeUnit, Advertisement, Speciality, Teacher, Course, OnlyContacted, Student, AttendedMockLesson


class TimeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=TimeUnit
        fields='__all__'


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Advertisement
        fields='__all__'


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Speciality
        fields='__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'


class OnlyContactedSerializer(serializers.ModelSerializer):
    class Meta:
        model=OnlyContacted
        fields='__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'


class AttendedMockLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttendedMockLesson
        fields='__all__'