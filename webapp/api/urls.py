from django.urls import path, include

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
    all_models_by_id
)


app_name = 'status_api'



urlpatterns = [
    path('prd/', all_models),
    path('prd/<int:id>/', all_models_by_id),
    
    path('select-field/', SelectFieldAPIView.as_view()),


    path('type-of-prd/', TypeOfPRDAPIView.as_view()),
    path('service-severity/', ServiceSeverityAPIView.as_view()),
    path('prd-discharge/', PRDDischargeLocationAPIView.as_view()),
    path('environ-factor/', EnvironmentFactorModifierAPIView.as_view()),
    path('protect-equip/', ProtectedEquipmentDemageStatusAPIView.as_view()),
    path('inspe-effect/', PRDInspectionEffectivenessAPIView.as_view()),
    path('overpres-demand/', OverPressureDemandCaseAPIView.as_view()),
]
