from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TypeOfPRDAPIView,
    ServiceSeverityAPIView,
    PRDDischargeLocationAPIView,
    ProtectedEquipmentDemageStatusAPIView,
    PRDInspectionEffectivenessAPIView,
    OverPressureDemandCaseAPIView,

    SelectFieldAPIView,

    EnvironmentFactorModifierAPIView,
    GeneralInformationAPIView,
    ProtectedFixedEquipmentAPIView,
    ConsequencesOfFailureInputDataAPIView,
    ConsequencesOfFailureOfLeakageAPIView,
    Prd_InspectionHistoryAPIView,
    ApplicableOverpressureDemandCaseAPIView,

    all_models,
    all_models_by_id,


)

from .views_2 import (
    GeneralInformationAPIView as GenInfo,
    ProtectedFixedEquipmentAPIView as ProtectFixed,
    Prd_InspectionHistoryAPIView as Prd_Inspe,

    all_models as joined_models,
    all_models_by_id as by_id,
    test_by_id,
    test_all,
    
    test_api,
    gen_data,
    
    ProjectRegistrationListView,
    ProjectRegistrationCreationView,
    ProjectRegistrationView,
)

from .serializers_2 import (
    AllModels,
    AllModelsById,

    models_by_id
)

app_name = 'status_api'


router = DefaultRouter()
router.register('prd', GenInfo, basename='GeneralInformationAPIView')
router.register('projects', ProjectRegistrationView, basename='ProjectRegistration')

urlpatterns = [
    path('', include(router.urls)),
    path('project/', ProjectRegistrationListView.as_view()),
    path('project/<int:pk>/', ProjectRegistrationCreationView.as_view()),
    
    path('test/', test_api, name='test_api'),
    path('submit/', gen_data, name='submit_data'),
    
    #path('gen/', GenInfo.as_view()),
    #path('protected/', ProtectFixed.as_view()),

    #path('all/', AllModels.as_view()),
    #path('all/<int:id>/', AllModelsById.as_view()),

    #path('prd/', joined_models),
    #path('prd/<int:id>/', by_id),
    
    #path('prd/<int:id>/', test_by_id),
    #path('prd/', test_all),


    path('type-of-prd/', TypeOfPRDAPIView.as_view()),
    path('service-severity/', ServiceSeverityAPIView.as_view()),
    path('prd-discharge/', PRDDischargeLocationAPIView.as_view()),
    path('environ-factor/', EnvironmentFactorModifierAPIView.as_view()),
    path('protect-equip/', ProtectedEquipmentDemageStatusAPIView.as_view()),
    path('inspe-effect/', PRDInspectionEffectivenessAPIView.as_view()),
    path('overpres-demand/', OverPressureDemandCaseAPIView.as_view()),
]
