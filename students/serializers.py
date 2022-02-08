from datetime import date
from rest_framework import serializers
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student, Penalty


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
        if date_stat:#please, provide date_stat in this format: ?date=2022-02-04
            representation['advertisement_statistics'] = instance.onlycontacted_set.filter(date_of_contacting__gte=date_stat).count()
        else:
            representation['advertisement_statistics'] = instance.onlycontacted_set.filter(date_of_contacting__lte=date.today()).count()

        return representation


class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model=Penalty
        fields=('id','name','penalty_in_percent','date_added')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }

    def validate_penalty_in_percent(self,value):
        if value < -100:
            raise serializers.ValidationError('Value can not be bigger then -100. It is the highest amount for discount!')
        return value

    def update(self,instance,validated_data):
        instance.name=validated_data.get('name')
        instance.penalty_in_percent = validated_data.get('penalty_in_percent')
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=True,queryset=Course.objects.all())
    class Meta:
        model=Teacher
        fields=('id','full_name', 'passport_id', 'photo', 'address', 'course','experience', 'time_unit')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }

        def validate_passport_id(self,value):
            if len(value) > 9:
                raise serializers.ValidationError('Length of passport id  can not be more than 9 characters!')
            return value

        def validate_photo(self,value):
            if not value.endswith('png') or not value.endswith('jpg'):
                raise serializers.ValidationError('Image should be in png or jpg format!')
            return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=('name', 'duration','time_unit','description', 'date_started', 'number_of_groups','cost_per_month', 'unit')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }

        def to_representation(self,instance):
            representation = super().to_representation(instance)
            representation['teacher_number'] = instance.teacher_set.all().count()
            representation['student_number'] = instance.student_set.all().count()


class OnlyContactedSerializer(serializers.ModelSerializer):
    course_interested = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    advertisement = serializers.PrimaryKeyRelatedField(many=True, queryset=Advertisement.objects.all())
    class Meta:
        model=OnlyContacted
        fields=('full_name', 'address', 'phone_number','course_interested', 'date_of_contacting','advertisement')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }


class StudentSerializer(serializers.ModelSerializer):
    selected_course = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    penalty = serializers.PrimaryKeyRelatedField(many=True, queryset=Penalty.objects.all())
    class Meta:
        model=Student
        fields=('id','student_id','only_contacted', 'photo', 'parent_phone_number', 'selected_course','has_paid_fee',
                'penalty', 'total_payment_per_month','unit1', 'total_loan_amount', 'unit2')
        extra_kwargs = {
            'id': {'read_only': 'True'},
        }

    def validate(self,data):
        if data['has_paid_fee']==True and data['total_loan_amount']>0:
            raise serializers.ValidationError('You can\'t pay tuition fee if you have loan')
        return data

    def validate_photo(self, value):
        if not value.endswith('png') or not value.endswith('jpg'):
            raise serializers.ValidationError('Image should be in png or jpg format!')
        return value


class StudentListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="only_contacted.full_name")
    phone_number = serializers.CharField(source="only_contacted.phone_number")
    class Meta:
        model = Student
        fields = (
        'student_id','full_name','phone_number','parent_phone_number')