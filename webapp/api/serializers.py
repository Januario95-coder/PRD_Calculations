from rest_framework import serializers

from webapp.models import (
    GeneralInformation,
    PrdInspection_TestHistory,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase
)
import os




class GeneralInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInformation
        fields = '__all__'


class ProtectedFixedEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrdInspection_TestHistory
        fields = '__all__'


class ConsequencesOfFailureInputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsequencesOfFailureInputData
        fields = '__all__'


class ConsequencesOfFailureOfLeakageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consequences0fFailureOfLeakage
        fields = '__all__'


class Prd_InspectionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Prd_InspectionHistory
        fields = '__all__'



class ApplicableOverpressureDemandCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicableOverpressureDemandCase
        fields = '__all__'


class GeneralSerializer(serializers.ModelSerializer):
    pass
