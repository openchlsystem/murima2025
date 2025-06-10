from rest_framework import serializers
from .models import ReferenceDataType, ReferenceData, ReferenceDataHistory


class ReferenceDataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceDataType
        fields = '__all__'


class ReferenceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceData
        fields = '__all__'


class ReferenceDataHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceDataHistory
        fields = '__all__'
