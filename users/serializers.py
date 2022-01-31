from rest_framework import serializers
from .models import EducationCentre


class EducationCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model=EducationCentre
        fields='__all__'