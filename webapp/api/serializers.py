from rest_framework import serializers
from drf_multiple_model.views import (
    ObjectMultipleModelAPIView
)

from webapp.models import (
    TypeOfPRD,
    ServiceSeverity,
    PRDDischargeLocation,
    EnvironmentFactorModifier,
    ProtectedEquipmentDemageStatus,
    PRDInspectionEffectiveness,
    OverPressureDemandCase,

    GeneralInformation,
    PrdInspection_TestHistory,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase
)
from ..IPRD_INPUT_CHOICES import IPRD_3_CHOICES
import os


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







def fetch_data(model, id):
    print(model.__name__)
    try:
        id_ = int(id)
        obj = model.objects.filter(id=id_)
    except (ValueError, TypeError):
        obj = model.objects.all()
    return obj


class AllModelsSerializer(ObjectMultipleModelAPIView):
    def get_querylist(self):
        try:
            id_ = self.request.query_params['id']
        except:
            id_ = None


        querylist = [
            {
                'queryset': fetch_data(GeneralInformation, id_),
                'serializer_class': GeneralInformationSerializer,
                'label': 'GeneralInformation'
            },
            {
                'queryset': fetch_data(PrdInspection_TestHistory, id_),
                'serializer_class': ProtectedFixedEquipmentSerializer,
                'label': 'ProtectedFixedEquipment'
            },
            {
                'queryset': fetch_data(ConsequencesOfFailureInputData, id_),
                'serializer_class': ConsequencesOfFailureInputDataSerializer,
                'label': 'ConsequencesOfFailureInputData'
            },
            {
                'queryset': fetch_data(Consequences0fFailureOfLeakage, id_),
                'serializer_class': ConsequencesOfFailureOfLeakageSerializer,
                'label': 'Consequences0fFailureOfLeakage'
            },
            {
                'queryset': fetch_data(Prd_InspectionHistory, id_),
                'serializer_class': Prd_InspectionHistorySerializer,
                'label': 'Prd_InspectionHistory'
            },
            {
                'queryset': fetch_data(ApplicableOverpressureDemandCase, id_),
                'serializer_class': ApplicableOverpressureDemandCaseSerializer,
                'label': 'ApplicableOverpressureDemandCase'
            },
        ]
        return querylist




