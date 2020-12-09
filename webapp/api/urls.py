from django.urls import path

from .views import (
    GeneralInformationAPIView,
    ProtectedFixedEquipmentAPIView,
    ConsequencesOfFailureInputDataAPIView,
    ConsequencesOfFailureOfLeakageAPIView,
    Prd_InspectionHistoryAPIView,
    ApplicableOverpressureDemandCaseAPIView
)


app_name = 'status_api'

urlpatterns = [
    path('gen-info/', GeneralInformationAPIView.as_view()),
    path('protected-equip/', ProtectedFixedEquipmentAPIView.as_view()),
    path('conseq-failure/', ConsequencesOfFailureInputDataAPIView.as_view()),
    path('conseq-leakage/', ConsequencesOfFailureOfLeakageAPIView.as_view()),
    path('insp-history/', Prd_InspectionHistoryAPIView.as_view()),
    path('overpressure-demand/', ApplicableOverpressureDemandCaseAPIView.as_view()),
]
