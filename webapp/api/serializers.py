from rest_framework import serializers


from webapp.models import (
    TypeOfPRD,
    ServiceSeverity,
    PRDDischargeLocation,
    EnvironmentFactorModifier,
    ProtectedEquipmentDemageStatus,
    PRDInspectionEffectiveness,
    OverPressureDemandCase,
    
    SelectField,

    GeneralInformation,
    PrdInspection_TestHistory,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase
)
from ..IPRD_INPUT_CHOICES import IPRD_3_CHOICES
import os


class SelectFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectField
        fields = '__all__'



class TypeOfPRDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfPRD
        fields = '__all__'


class ServiceSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSeverity
        fields = '__all__'


class PRDDischargeLocationSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = PRDDischargeLocation
        fields = '__all__'

class EnvironmentFactorModifierSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = EnvironmentFactorModifier
        fields = '__all__'

class ProtectedEquipmentDemageStatusSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = ProtectedEquipmentDemageStatus
        fields = '__all__'


class PRDInspectionEffectivenessSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = PRDInspectionEffectiveness
        fields = '__all__'


class OverPressureDemandCaseSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = OverPressureDemandCase
        fields = '__all__'








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





















