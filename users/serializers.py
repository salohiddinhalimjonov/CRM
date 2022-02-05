from rest_framework import serializers
from .models import EducationCentre
from datetime import datetime

class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=64, write_only=True, required=True)
    password2=serializers.CharField(max_length=64, write_only=True, required=True)

    class Meta:
        model=EducationCentre
        fields=('ECemail', 'ECname', 'EClocation', 'ECphonenumber','password1', 'password2')

    # Sometimes you may need to access a serializer’s raw input. It’s either because data has been already modified by running serializer.is_valid(),
    # or it’s needed to compare the value of another field in a validation method when validated_data is not yet available.
    # It can be achieved by accessing serializer.initial_data, which stores raw input as a Dict, as shown in this example:
    def validate_password1(self,password1):
        if password1!=self.initial_data['password2']:
            raise serializers.ValidationError('Passwords do not match!')
        return password1


class UserPasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(max_length=64, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=64, write_only=True, required=True)
    #old_password = serializers.CharField(max_length=64, write_only=True, required=True)

    # def validate_old_password(self, value):
    #     user = self.context['request'].user
    #     if not user.check_password(value):
    #         raise serializers.ValidationError('Your old password is incorrect')
    #     return value

    def validate(self,data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('New Passwords do not match')
        return data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=EducationCentre
        fields=('id','ECemail', 'ECname', 'EClocation', 'ECphonenumber', 'date_joined')
        extra_kwargs = {
            'id':{'read_only': 'True'},
            'date_joined':{'read_only': 'True'}
        }
#     If I dont write update() method inside the serializer class I have to create object in views.py(like, EducationCentre.objects.create_user(**serializer.validated_data))
    #If I write this method, I just give it incoming data and save it like this(serializer.save()) after checking for validation(is_valid=True)
    #when I call serializer.save() in views.py it will come to serializer in serializers.py and calls update or create method
    # In model serializer, these metohds are automatically created, so I can use it without creating, If I want to change some points I have to create
    #these methods also in model serializer like this \/

    def update(self,instance, validated_data):
        instance.ECemail = validated_data['ECemail']
        instance.ECname = validated_data['ECname']
        instance.EClocation = validated_data['EClocation']
        instance.ECphonenumber = validated_data['ECphonenumber']
        instance.save()
        return instance
# instance is model object instance that is being updated. validated_data - we can call this when to call serializer.is_valid() returns True and data
# is given inside serializer. It returns the incoming data items that has the valid value.(if value is not required in serializer and so it returns None
# this item is not included in validated_data)

class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model=EducationCentre
        fields='__all__'

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['teachers'] = instance.teacher_set.all().count()
        representation['courses'] = instance.course_set.all().count()
        representation['students'] = instance.onlycontacted_set.filter(has_been_student=True)
        return representation

#https://stackoverflow.com/questions/42000687/what-are-the-differences-between-data-and-validated-data
