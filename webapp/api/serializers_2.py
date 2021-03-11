from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_multiple_model.views import (
    ObjectMultipleModelAPIView,
    FlatMultipleModelAPIView
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
    ConsequencesOfFailureOfLeakage,
    Prd_InspectionHistory,
    ApplicableOverpressureDemandCase,
    
    ProjectRegistration,
    AllModels,
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
        fields = ['id', 'name']


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
        fields = ['id', 'name']


class PRDInspectionEffectivenessSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = PRDInspectionEffectiveness
        fields = ['id', 'name']


class OverPressureDemandCaseSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = OverPressureDemandCase
        fields = '__all__'



class ProtectedFixedEquipmentSerializer(serializers.ModelSerializer):
    Protected_Equipment_Demage_Status = ProtectedEquipmentDemageStatusSerializer()

    class Meta:
        model = ProtectedFixedEquipmentPipingData
        fields = '__all__' #['id', 'Fixed_Equipment_Protected_by_PRD',
                  #'Maximum_Allow_able_Working_Pressure_of_Protected_Equipment',
                  #'Operating_Pressure_of_the_Protected_Equipment',
                  #'management_system_factor',
                  #'Protected_Equipment_Demage_Status']


class ConsequencesOfFailureInputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsequencesOfFailureInputData
        fields = '__all__'


class ConsequencesOfFailureOfLeakageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsequencesOfFailureOfLeakage
        fields = '__all__'


class Prd_InspectionHistorySerializer(serializers.ModelSerializer):
    PRD_Inspection_Effectiveness = PRDInspectionEffectivenessSerializer()

    class Meta:
        model = Prd_InspectionHistory
        fields = ['id', 'RBI_inspection_test_date',
                  'PRD_pop_test_results', 'PRD_Leakage_results',
                  'PRD_Overhauled_during_the_inspection',
                  'PRD_replace_with_new_PRD_in_lieu_of_overhaul',
                  'PRD_Inspection_Effectiveness']



class ApplicableOverpressureDemandCaseSerializer(serializers.ModelSerializer):
    Over_pressure_demand_case = OverPressureDemandCaseSerializer()

    class Meta:
        model = ApplicableOverpressureDemandCase
        fields = ['id', 'Overpressure_associated_with_the_overpressure',
                  'PRD_COF_to_open_associated_with_jth_overpressure',
                  'Over_pressure_demand_case']
                  
   

def get_Protected_Equipment(model, serializer, id=None):
    items = model.objects.all()
    if id is not None:
        items = items.filter(id=id).first()
        if items is None:
            return {}
        return serializer(items).data
    return serializer(items, many=True).data
    

class GeneralInformationSerializer(serializers.ModelSerializer):
    Type_of_PRD = TypeOfPRDSerializer()
    Service_severity = ServiceSeveritySerializer()
    PRD_Discharge_Location = PRDDischargeLocationSerializer()
    Environment_Factor_Modifier = EnvironmentFactorModifierSerializer()

    class Meta:
        model = GeneralInformation
        fields = ['id', 'PRD_identification_number', 'PRD_function',
                  'Installation_of_PRD', 'RBI_assessment_date',
                  'Type_of_PRD', 'PRD_Containing_Soft_Seats',
                  'PRD_set', 'Service_severity',
                  'PRD_Discharge_Location', 'Environment_Factor_Modifier',
                  'Rupture_disk_is_installed_upstream_of_PRD']
                  
        
    def to_representation(self, instance):
        id = None
        try:
            id = instance.id
        except:
            id = None
        data = super().to_representation(instance)
        #data['ProtectedFixedEquipmentPipingData'] = get_Protected_Equipment(ProtectedFixedEquipmentPipingData, ProtectedFixedEquipmentSerializer, id=id)  #ProtectedFixedEquipmentSerializer(ProtectedFixedEquipmentPipingData.objects.all()).data
        #data['ConsequencesOfFailureInputData'] = get_Protected_Equipment(ConsequencesOfFailureInputData, ConsequencesOfFailureInputDataSerializer, id=id)
        #data['Consequences0fFailureOfLeakage'] = get_Protected_Equipment(Consequences0fFailureOfLeakage, ConsequencesOfFailureOfLeakageSerializer, id=id)
        #data['Prd_InspectionHistory'] = get_Protected_Equipment(Prd_InspectionHistory, Prd_InspectionHistorySerializer, id=id)
        #data['ApplicableOverpressureDemandCase'] = get_Protected_Equipment(ApplicableOverpressureDemandCase, ApplicableOverpressureDemandCaseSerializer, id=id)
        return data



class AllModelsSerializer(serializers.ModelSerializer):
    general_information = GeneralInformationSerializer()
    protected_fixed_equip = ProtectedFixedEquipmentSerializer()
    consequence_of_failure_input_data = ConsequencesOfFailureInputDataSerializer()
    consequence_of_failure_leakage = ConsequencesOfFailureOfLeakageSerializer()
    PRD_Inspection_history = Prd_InspectionHistorySerializer(many=True)
    applicable_overpressure_demand = ApplicableOverpressureDemandCaseSerializer()
    
    class Meta:
        model = AllModels
        fields = ['general_information', 'protected_fixed_equip',
                  'consequence_of_failure_input_data',
                  'consequence_of_failure_leakage',
                  'PRD_Inspection_history',
                  'applicable_overpressure_demand']


class ProjectRegistrationSerializer(serializers.ModelSerializer):
    # project = AllModelsSerializer()
    
    class Meta:
        model = ProjectRegistration
        fields = ['project_name', 'project_function',
                  'creation_date'] #, 'project']



class AllModels(ObjectMultipleModelAPIView):
    #add_model_type = False

    querylist = [
        {'queryset': GeneralInformation.objects.all(),
         'serializer_class': GeneralInformationSerializer},
        {'queryset': ProtectedFixedEquipmentPipingData.objects.all(),
         'serializer_class': ProtectedFixedEquipmentSerializer},
        {'queryset': ConsequencesOfFailureInputData.objects.all(),
         'serializer_class': ConsequencesOfFailureInputDataSerializer},
        {'queryset': ConsequencesOfFailureInputData.objects.all(),
         'serializer_class': ConsequencesOfFailureOfLeakageSerializer},
         {'queryset': Prd_InspectionHistory.objects.all(),
         'serializer_class': Prd_InspectionHistorySerializer},
        {'queryset': ApplicableOverpressureDemandCase.objects.all(),
         'serializer_class': ApplicableOverpressureDemandCaseSerializer}
    ]


def check_by_id(model, modelname):
    check = list(model) == []

    if check:
        model = {}
    else:
        model = model.serialize()[0]

    return {f'{modelname}': model}



class AllModelsById(ObjectMultipleModelAPIView):
    #add_model_type = True

    def get_querylist(self):
        id_ = self.request._request.path.split('/')[-2]

        gen = GeneralInformation.objects.filter(id=int(id_))
        protect_fixed = ProtectedFixedEquipmentPipingData.objects.filter(id=int(id_))
        conseq_failure_input = ConsequencesOfFailureInputData.objects.filter(id=int(id_))
        conseq_failure_leakage = Consequences0fFailureOfLeakage.objects.filter(id=int(id_))
        prd_inspect = Prd_InspectionHistory.objects.filter(id=int(id_))
        applic_overpressure = ApplicableOverpressureDemandCase.objects.filter(id=int(id_))

        data = {}
        data.update(check_by_id(gen, 'GeneralInformation'))
        data.update(check_by_id(protect_fixed, 'ProtectedFixedEquipmentPipingData'))
        data.update(check_by_id(conseq_failure_input, 'ConsequencesOfFailureInputData'))
        data.update(check_by_id(conseq_failure_leakage, 'Consequences0fFailureOfLeakage'))
        data.update(check_by_id(prd_inspect, 'Prd_InspectionHistory'))
        data.update(check_by_id(applic_overpressure, 'ApplicableOverpressureDemandCase'))


        # data = gen.serialize()[0].copy()
        # #for val1, val2, val3, val4, val5, val6 in zip(protect_fixed.serialize(),
        #                                               #conseq_failure_input.serialize(),
        #                                               #conseq_failure_leakage.serialize(),
        #                                               #prd_inspect.serialize(),
        #                                               #applic_overpressure.serialize()):
        # data.update({'ProtectedFixedEquipmentPipingData': protect_fixed.serialize()[0]})
        # data.update({'ConsequencesOfFailureInputData': conseq_failure_input.serialize()[0]})
        # data.update({'Consequences0fFailureOfLeakage': conseq_failure_leakage.serialize()[0]})
        # data.update({'Prd_InspectionHistory': prd_inspect.serialize()[0]})
        # data.update({'ApplicableOverpressureDemandCase': applic_overpressure.serialize()[0]})
        # print('\n')
        data = [val for val in data.values()]
        # print('\n')

        querylist = [
            {'queryset': GeneralInformation.objects.filter(id=int(id_)),
             'serializer_class': GeneralInformationSerializer},
            {'queryset': ProtectedFixedEquipmentPipingData.objects.filter(id=int(id_)),
             'serializer_class': ProtectedFixedEquipmentSerializer},
            {'queryset': ConsequencesOfFailureInputData.objects.filter(id=int(id_)),
             'serializer_class': ConsequencesOfFailureInputDataSerializer},
            {'queryset': Consequences0fFailureOfLeakage.objects.filter(id=int(id_)),
             'serializer_class': ConsequencesOfFailureOfLeakageSerializer},
            {'queryset': Prd_InspectionHistory.objects.filter(id=int(id_)),
             'serializer_class': Prd_InspectionHistorySerializer},
            {'queryset': ApplicableOverpressureDemandCase.objects.filter(id=int(id_)),
             'serializer_class': ApplicableOverpressureDemandCaseSerializer}
        ]

        return querylist



@api_view(['GET'])
def models_by_id(request, id):
    gen = GeneralInformation.objects.filter(id=int(id))
    protect_fixed = ProtectedFixedEquipmentPipingData.objects.filter(id=int(id))
    conseq_failure_input = ConsequencesOfFailureInputData.objects.filter(id=int(id))
    conseq_failure_leakage = Consequences0fFailureOfLeakage.objects.filter(id=int(id))
    prd_inspect = Prd_InspectionHistory.objects.filter(id=int(id))
    applic_overpressure = ApplicableOverpressureDemandCase.objects.filter(id=int(id))

    data = {}
    data.update(check_by_id(gen, 'GeneralInformation'))
    data.update(check_by_id(protect_fixed, 'ProtectedFixedEquipmentPipingData'))
    data.update(check_by_id(conseq_failure_input, 'ConsequencesOfFailureInputData'))
    data.update(check_by_id(conseq_failure_leakage, 'Consequences0fFailureOfLeakage'))
    data.update(check_by_id(prd_inspect, 'Prd_InspectionHistory'))
    data.update(check_by_id(applic_overpressure, 'ApplicableOverpressureDemandCase'))
    #print(data)

    return Response(data)
    
    
    

    

  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
