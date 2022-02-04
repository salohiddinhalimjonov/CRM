from datetime import date
from rest_framework import serializers
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student, AttendedMockLesson


class TimeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=TimeUnit
        fields=('id','name')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Advertisement
        fields=('id','name', 'date_added')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        date_stat = self.context['request'].query_params.get('date')
        if date_stat:
            representation['advertisement_statistics'] = instance.onlycontacted_set.filter(date_of_contacting__gte=date_stat).count()
        else:
            representation['advertisement_statistics'] = instance.onlycontacted_set.filter(date_of_contacting__lte=date.today()).count()

        return representation


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

