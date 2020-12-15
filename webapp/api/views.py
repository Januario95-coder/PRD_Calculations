from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    generics, mixins, permissions
)

from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication

from .serializers import (
    TypeOfPRDSerializer,
    PRDDischargeLocationSerializer,
    ServiceSeveritySerializer,
    EnvironmentFactorModifierSerializer,
    ProtectedEquipmentDemageStatusSerializer,
    PRDInspectionEffectivenessSerializer,
    OverPressureDemandCaseSerializer,

    GeneralInformationSerializer,
    ProtectedFixedEquipmentSerializer,
    ConsequencesOfFailureInputDataSerializer,
    ConsequencesOfFailureOfLeakageSerializer,
    Prd_InspectionHistorySerializer,
    ApplicableOverpressureDemandCaseSerializer
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

import json

Type_of_PRD = {
    'convention_spring_loaded': 'Convention Spring-Loaded',
    'balanced_bellows': 'Balanced Bellows',
    'pilot_operated': 'Pilot Operated',
    'Rupture_disk_only': 'Rupture Disk Only'
}



def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid



class TypeOfPRDAPIView(generics.ListAPIView):
    serializer_class = TypeOfPRDSerializer
    queryset = TypeOfPRD.objects.all()


class ServiceSeverityAPIView(generics.ListAPIView):
    serializer_class = ServiceSeveritySerializer
    queryset = ServiceSeverity.objects.all()


class PRDDischargeLocationAPIView(generics.ListAPIView):
    serializer_class = PRDDischargeLocationSerializer
    queryset = PRDDischargeLocation.objects.all()


class EnvironmentFactorModifierAPIView(generics.ListAPIView):
    serializer_class = EnvironmentFactorModifierSerializer
    queryset = EnvironmentFactorModifier.objects.all()


class ProtectedEquipmentDemageStatusAPIView(generics.ListAPIView):
    serializer_class = ProtectedEquipmentDemageStatusSerializer
    queryset = ProtectedEquipmentDemageStatus.objects.all()

class PRDInspectionEffectivenessAPIView(generics.ListAPIView):
    serializer_class = PRDInspectionEffectivenessSerializer
    queryset = PRDInspectionEffectiveness.objects.all()

class OverPressureDemandCaseAPIView(generics.ListAPIView):
    serializer_class = OverPressureDemandCaseSerializer
    queryset = OverPressureDemandCase.objects.all()





class GeneralInformationAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    serializer_class = GeneralInformationSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = GeneralInformation.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ProtectedFixedEquipmentAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
    serializer_class = ProtectedFixedEquipmentSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = PrdInspection_TestHistory.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConsequencesOfFailureInputDataAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
    serializer_class = ConsequencesOfFailureInputDataSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = ConsequencesOfFailureInputData.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ConsequencesOfFailureOfLeakageAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
    serializer_class = ConsequencesOfFailureOfLeakageSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Consequences0fFailureOfLeakage.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class Prd_InspectionHistoryAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
    serializer_class = Prd_InspectionHistorySerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Prd_InspectionHistory.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ApplicableOverpressureDemandCaseAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
    serializer_class = ApplicableOverpressureDemandCaseSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = ApplicableOverpressureDemandCase.objects.all()
        # print(request.user)
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
