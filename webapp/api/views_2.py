from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import (
    generics, mixins, permissions
)
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication

import json
import requests


from .serializers_2 import (
    TypeOfPRDSerializer,
    PRDDischargeLocationSerializer,
    ServiceSeveritySerializer,
    EnvironmentFactorModifierSerializer,
    ProtectedEquipmentDemageStatusSerializer,
    PRDInspectionEffectivenessSerializer,
    OverPressureDemandCaseSerializer,

    SelectFieldSerializer,

    GeneralInformationSerializer,
    ProtectedFixedEquipmentSerializer,
    ConsequencesOfFailureInputDataSerializer,
    ConsequencesOfFailureOfLeakageSerializer,
    Prd_InspectionHistorySerializer,
    ApplicableOverpressureDemandCaseSerializer,
)

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
    ProtectedFixedEquipmentPipingData,
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



class SelectFieldAPIView(generics.ListAPIView):
    serializer_class = SelectFieldSerializer
    queryset = SelectField.objects.all()



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





class GeneralInformationAPIView(ModelViewSet):
    queryset = GeneralInformation.objects.all()
    serializer_class = GeneralInformationSerializer
    



class ProtectedFixedEquipmentAPIView(generics.ListCreateAPIView):
    queryset = ProtectedFixedEquipmentPipingData.objects.all()
    serializer_class = ProtectedFixedEquipmentSerializer
    



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



def fetch_data(model, id=None):
    objs = model.objects.all()
    if id is not None:
        objs = objs.filter(id=id)


    return objs





@api_view(['GET'])
def all_models(request):
    gen = fetch_data(GeneralInformation)
    prd_inspe = fetch_data(ProtectedFixedEquipmentPipingData)
    histo = fetch_data(ConsequencesOfFailureInputData)
    conseq_failure = fetch_data(Consequences0fFailureOfLeakage)
    prd_hist = fetch_data(Prd_InspectionHistory)
    appl_dem = fetch_data(ApplicableOverpressureDemandCase)

    data = []
    for val1, val2, val3 in zip(gen.serialize(),
                                prd_inspe.serialize(),
                                histo.serialize()):
                                                  #conseq_failure.serialize(),
                                                  #prd_hist.serialize(),
                                                  #appl_dem.serialize()):

        val1.update({'ProtectedFixedEquipmentPipingData': val2})
        val1.update({'ConsequencesOfFailureInputData': val3})
        #val1.update({'Consequences0fFailureOfLeakage': val4})
        #val1.update({'Prd_InspectionHistory': val5})
        #val1.update({'ApplicableOverpressureDemandCase': val6})
        data.append(val1)
        
    print(data)


    return Response(
        data
    )



@api_view(['GET'])
def all_models_by_id(request, id):
    gen = fetch_data(GeneralInformation, id=id)
    prd_inspe = fetch_data(ProtectedFixedEquipmentPipingData, id=id)
    #conseq_failure = fetch_data(ConsequencesOfFailureInputData, id=id)
    #conseq_leakage = fetch_data(Consequences0fFailureOfLeakage, id=id)
    #prd_hist = fetch_data(Prd_InspectionHistory, id=id)
    #appl_dem = fetch_data(ApplicableOverpressureDemandCase, id=id)

    try:
        data = gen.serialize()[0].copy()
        data.update({'ProtectedFixedEquipmentPipingData': prd_inspe.serialize()[0]})
        #data.update({'ConsequencesOfFailureInputData': conseq_failure.serialize()[0]})
        #data.update({'Consequences0fFailureOfLeakage': conseq_leakage.serialize()[0]})
        #data.update({'Prd_InspectionHistory': prd_hist.serialize()[0]})
        #data.update({'ApplicableOverpressureDemandCase': appl_dem.serialize()[0]})

    except:
        data = [{}]


    return Response(
        data
    )



def check_by_id(model, modelname):
    check = list(model) == []

    if check:
        model = {}
    else:
        model = model.serialize()[0]

    return {f'{modelname}': model}
    


@api_view(['GET'])
def test_by_id(request, id):
    url = f'http://127.0.0.1:8000/api/all/{id}/'
    r = requests.get(url)
    data = r.json()
    all_data = []
    try:
        data = [val[0] for val in data.values()]
        all_data = data[0]
        all_data.update({'ProtectedFixedEquipmentPipingData': data[1]})
        all_data.update({'ConsequencesOfFailureInputData': data[2]})
        all_data.update({'Consequences0fFailureOfLeakage': data[3]})
        all_data.update({'Prd_InspectionHistory': data[4]})
        all_data.update({'ApplicableOverpressureDemandCase': data[5]})
    except IndexError:
        all_data = [{}]
    return Response(all_data)
    
    
    
    

@api_view(['GET'])
def test_all(request):
    url = 'http://127.0.0.1:8000/api/all/'
    r = requests.get(url)
    data = r.json()
    all_data = []
    try:
        data_ = data.values()
        count = 0
        gen, protect_fixed, conseq_failure_input, conseq_failure_leakage, prd_inspect, applic_overpressure = data_
        for val1, val2, val3, val4, val5, val6 in zip(gen, 
                                                      protect_fixed,
                                                      conseq_failure_input,
                                                      conseq_failure_leakage,
                                                      prd_inspect,
                                                      applic_overpressure):
            all_data.append({})
            all_data[count].update(val1)
            all_data[count].update({'ProtectedFixedEquipmentPipingData': val2})
            all_data[count].update({'ConsequencesOfFailureInputData': val3})
            all_data[count].update({'Consequences0fFailureOfLeakage': val4})
            all_data[count].update({'Prd_InspectionHistory': val5})
            all_data[count].update({'ApplicableOverpressureDemandCase': val6})
            count += 1
            
    except IndexError:
        all_data = [{}]
    return Response(all_data)
    











