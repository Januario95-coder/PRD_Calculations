from django.urls import path

from .views import (
    TypeOfPRDAPIView,
    ServiceSeverityAPIView,
    PRDDischargeLocationAPIView,
    ProtectedEquipmentDemageStatusAPIView,
    PRDInspectionEffectivenessAPIView,
    OverPressureDemandCaseAPIView,

    EnvironmentFactorModifierAPIView,
    GeneralInformationAPIView,
    ProtectedFixedEquipmentAPIView,
    ConsequencesOfFailureInputDataAPIView,
    ConsequencesOfFailureOfLeakageAPIView,
    Prd_InspectionHistoryAPIView,
    ApplicableOverpressureDemandCaseAPIView
)


app_name = 'status_api'

urlpatterns = [
    path('type-of-prd/', TypeOfPRDAPIView.as_view()),
    path('service-severity/', ServiceSeverityAPIView.as_view()),
    path('prd-discharge/', PRDDischargeLocationAPIView.as_view()),
    path('environ-factor/', EnvironmentFactorModifierAPIView.as_view()),
    path('protect-equip/', ProtectedEquipmentDemageStatusAPIView.as_view()),
    path('inspe-effect/', PRDInspectionEffectivenessAPIView.as_view()),
    path('overpres-demand/', OverPressureDemandCaseAPIView.as_view()),

    path('gen-info/', GeneralInformationAPIView.as_view()),
    path('protected-equip/', ProtectedFixedEquipmentAPIView.as_view()),
    path('conseq-failure/', ConsequencesOfFailureInputDataAPIView.as_view()),
    path('conseq-leakage/', ConsequencesOfFailureOfLeakageAPIView.as_view()),
    path('insp-history/', Prd_InspectionHistoryAPIView.as_view()),
    path('overpressure-demand/', ApplicableOverpressureDemandCaseAPIView.as_view()),
]
