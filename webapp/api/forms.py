from django import forms 
from webapp.IPRD_INPUT_CHOICES import *


class DateInput(forms.DateTimeInput):
    format_key = '%Y-%m-%dT%S:%M:%S'
    input_type = 'date'


class GenInfoForm(forms.Form):
    id = forms.IntegerField()
    PRD_identification_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'value': 'ACD1234'
        })  
    )
    PRD_function = forms.CharField(
        widget=forms.TextInput(attrs={
            'value': 'ARG123'
        })
    )
    # Installation_of_PRD = forms.DateTimeField(
        # widget=DateInput()
    # )
    # RBI_assessment_date = forms.DateTimeField(
        # widget=DateInput()
    # )
    Type_of_PRD = forms.ChoiceField(choices=IPRD_3_CHOICES)
    PRD_Containing_Soft_Seats = forms.ChoiceField(choices=IPRD_4_CHOICES)
    PRD_set = forms.CharField()
    Service_severity = forms.ChoiceField(choices=IPRD_6_CHOICES)
    PRD_Discharge_Location = forms.ChoiceField(choices=IPRD_7_CHOICES)
    Environment_Factor_Modifier = forms.ChoiceField(choices=IPRD_8_CHOICES)
    Rupture_disk_is_installed_upstream_of_PRD = forms.ChoiceField(choices=IPRD_9_CHOICES)