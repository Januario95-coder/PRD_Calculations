from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    generics, mixins, permissions
)

from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication

from .serializers import (
    GeneralInformationSerializer,
    ProtectedFixedEquipmentSerializer,
    ConsequencesOfFailureInputDataSerializer,
    ConsequencesOfFailureOfLeakageSerializer,
    Prd_InspectionHistorySerializer,
    ApplicableOverpressureDemandCaseSerializer
)
from webapp.models import (
    GeneralInformation,
    PrdInspection_TestHistory,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase
)

import json



def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid



class GeneralInformationAPIView(
    mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # IsAuthenticated
    # authentication_classes = [SessionAuthentication]
    # Override queryset
    # queryset = GeneralInformation.objects.all()
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
