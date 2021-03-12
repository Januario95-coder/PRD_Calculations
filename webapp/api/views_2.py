from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import (
    generics, mixins, permissions
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


import json
import requests
import datetime 
from datetime import datetime as dt


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
    
    ProjectRegistrationSerializer,
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
    ConsequencesOfFailureInputData,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase,
    
    ProjectRegistration,
)

from .forms import GenInfoForm

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
    

def test_submission(request):
    if request.method == 'POST':
        form = GenInfoForm(request.POST)
        print(request.body)
        if form.is_valid():
            print('\nForm is valid')
            data = form.cleaned_data
            form.save(commit=True)
            
            # data['Installation_of_PRD'] = data['Installation_of_PRD'].strftime('%Y-%m:%d %H:%M:%S')
            # data['RBI_assessment_date'] = data['RBI_assessment_date'].strftime('%Y-%m:%d %H:%M:%S')
            print(data, '\n')
    else:
        form = GenInfoForm()
        print('Form is not valid')
        
    return render(request, 
                  'webapp/testSubmission/testSubmission.html',
                  {'form': form})




@require_POST
@csrf_exempt
def gen_data(request):
    data = json.loads(request.body)
    print('\nSubmitted data:')
    print(data)
    print()
    
    form = GenInfoForm(data)
    print(f'Form is valid: {form.is_valid()}')
    message = ''
    
    # obj = GeneralInformation.objects.filter(id=data['id'])
    # if obj.exists():
        # data = form.cleaned_data
        # obj = obj.first()
        # obj.PRD_identification_number = data['PRD_identification_number']
        # obj.PRD_function = data['PRD_function']
        # obj.Installation_of_PRD = data['Installation_of_PRD']
        # obj.RBI_assessment_date = data['RBI_assessment_date']
        # obj.Type_of_PRD = TypeOfPRD.objects.get(name=data['Type_of_PRD'])
        # obj.PRD_Containing_Soft_Seats = data['PRD_Containing_Soft_Seats']
        # obj.PRD_set = data['PRD_set']
        # obj.Service_severity = ServiceSeverity.objects.get(name=data['Service_severity'])
        # obj.PRD_Discharge_Location = PRDDischargeLocation.objects.get(name=data['PRD_Discharge_Location'])
        # obj.Environment_Factor_Modifier = EnvironmentFactorModifier.objects.get(name=data['Environment_Factor_Modifier'])
        # obj.Rupture_disk_is_installed_upstream_of_PRD = data['Rupture_disk_is_installed_upstream_of_PRD']
        # obj.save()
        # message = 'Object updated successfully'
    # else:
        # message = 'Object was not updated'
    
    
    if form.is_valid():
        print('Cleaned data:')
        data = form.cleaned_data
        print(data)
        id_number = data['id']
        obj = GeneralInformation.objects.filter(id=id_number)
        if obj.exists():
            obj = obj.first()
            obj.PRD_identification_number = data['PRD_identification_number']
            obj.PRD_function = data['PRD_function']
            obj.Installation_of_PRD = data['Installation_of_PRD']
            obj.RBI_assessment_date = data['RBI_assessment_date']
            obj.Type_of_PRD = TypeOfPRD.objects.get(name=data['Type_of_PRD'])
            obj.PRD_Containing_Soft_Seats = data['PRD_Containing_Soft_Seats']
            obj.PRD_set = data['PRD_set']
            obj.Service_severity = ServiceSeverity.objects.get(name=data['Service_severity'])
            obj.PRD_Discharge_Location = PRDDischargeLocation.objects.get(name=data['PRD_Discharge_Location'])
            obj.Environment_Factor_Modifier = EnvironmentFactorModifier.objects.get(name=data['Environment_Factor_Modifier'])
            obj.Rupture_disk_is_installed_upstream_of_PRD = data['Rupture_disk_is_installed_upstream_of_PRD']
            obj.save()
            message = f'Object updated successfully'
        else:
            message = 'Object was not updated'
    else:
        message = 'form is not valid'
    print('\n', message)
    return JsonResponse({
        'message': message
    })

   

def test_api(request):
    if request.method == 'POST':
        form = GenInfoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(form.is_valid())
            print(data)
            """
            id_number = data['PRD_identification_number']
            obj = GeneralInformation.objects.filter(PRD_identification_number=id_number)
            if obj.exists():
                obj = obj.first()
                obj.PRD_identification_number = id_number
                obj.PRD_function = data['PRD_function']
                obj.Installation_of_PRD = data['Installation_of_PRD']
                obj.RBI_assessment_date = data['RBI_assessment_date']
                obj.Type_of_PRD = TypeOfPRD.objects.get(name=data['Type_of_PRD'])
                obj.PRD_Containing_Soft_Seats = data['PRD_Containing_Soft_Seats']
                obj.PRD_set = data['PRD_set']
                obj.Service_severity = ServiceSeverity.objects.get(name=data['Service_severity'])
                obj.PRD_Discharge_Location = PRDDischargeLocation.objects.get(name=data['PRD_Discharge_Location'])
                obj.Environment_Factor_Modifier = EnvironmentFactorModifier.objects.get(name=data['Environment_Factor_Modifier'])
                obj.Rupture_disk_is_installed_upstream_of_PRD = data['Rupture_disk_is_installed_upstream_of_PRD']
                obj.save()
            else:
                obj = GeneralInformation.objects.create(
                    PRD_identification_number = id_number,
                    PRD_function = data['PRD_function'],
                    Installation_of_PRD = data['Installation_of_PRD'],
                    RBI_assessment_date = data['RBI_assessment_date'],
                    Type_of_PRD = TypeOfPRD.objects.get(name=data['Type_of_PRD']),
                    PRD_Containing_Soft_Seats = data['PRD_Containing_Soft_Seats'],
                    PRD_set = data['PRD_set'],
                    Service_severity = ServiceSeverity.objects.get(name=data['Service_severity']),
                    PRD_Discharge_Location = PRDDischargeLocation.objects.get(name=data['PRD_Discharge_Location']),
                    Environment_Factor_Modifier = EnvironmentFactorModifier.objects.get(name=data['Environment_Factor_Modifier']),
                    Rupture_disk_is_installed_upstream_of_PRD = data['Rupture_disk_is_installed_upstream_of_PRD']
                )
                obj.save()
                """
            #print(id_number)
            #RESDF
    else:
        form = GenInfoForm()
    return render(request,
                  'webapp/test.html',
                  {'form': form})






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



class ProjectRegistrationView(ModelViewSet):
    queryset = ProjectRegistration.objects.all()
    serializer_class = ProjectRegistrationSerializer
    


class ProjectRegistrationListView(generics.ListAPIView):
    queryset = ProjectRegistration.objects.all()
    serializer_class = ProjectRegistrationSerializer
    
    
class ProjectRegistrationCreationView(
              generics.RetrieveAPIView,
              generics.UpdateAPIView):
    queryset = ProjectRegistration.objects.all()
    serializer_class = ProjectRegistrationSerializer    




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
    











