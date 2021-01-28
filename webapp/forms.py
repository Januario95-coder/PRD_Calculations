from .models import (
    GeneralInformation,
    ProtectedFixedEquipmentPipingData,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    ApplicableOverpressureDemandCase,
    Prd_InspectionHistory
)
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(
            attrs={
                'id': 'username',
                'class': 'login-inputs',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(max_length=15,
        widget=forms.PasswordInput(
            attrs={
                'id': 'user-password',
                'class': 'login-inputs',
                'placeholder': 'Password'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError('Wrong username or password')
        return username


    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Wrong password')
        return password


    # def clean(self):
    #     data = self.cleaned_data
    #     password = self.cleaned_data.get('password')
    #     username = self.cleaned_data.get('username')
    #     user = authenticate(username=username, password=password)
    #     print(user is None)
    #     if user is not None:
    #         return data
    #     else:
    #         raise forms.ValidationError('Wrong password')




class DateInput(forms.DateInput):
    format_key = '%Y-%m-%d'
    input_type = 'date'



class GeneralInformationForm(forms.ModelForm):
    # Installation_of_PRD = forms.DateField(
    #     widget=DateInput
    # )
    # RBI_assessment_date = forms.DateField(
    #     widget=DateInput
    # )

    def __init__(self, *args, **kwargs):
        super(GeneralInformationForm, self).__init__(*args, **kwargs)
        self.fields['PRD_identification_number'].required = False
        self.fields['PRD_function'].required = False
        self.fields['Installation_of_PRD'].required = False
        self.fields['RBI_assessment_date'].required = False
        self.fields['Type_of_PRD'].required = False
        self.fields['PRD_Containing_Soft_Seats'].required = False
        # self.fields['PRD_set'].required = False
        self.fields['Service_severity'].required = False
        self.fields['PRD_Discharge_Location'].required = False
        self.fields['Environment_Factor_Modifier'].required = False
        self.fields['Rupture_disk_is_installed_upstream_of_PRD'].required = False

    class Meta:
        model = GeneralInformation
        widgets = {
            'Installation_of_PRD': DateInput(),
            'RBI_assessment_date': DateInput()
        }

        fields = ['PRD_identification_number', 'PRD_function',
                  'Installation_of_PRD', 'RBI_assessment_date',
                  'Type_of_PRD', 'PRD_Containing_Soft_Seats',
                  'PRD_set', 'Service_severity',
                  'PRD_Discharge_Location', 'Environment_Factor_Modifier',
                  'Rupture_disk_is_installed_upstream_of_PRD'
                ]


class ProtectedFixedEquipmentPipingDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PRD_InspectionForm, self).__init__(*args, **kwargs)
        self.fields['Fixed_Equipment_Protected_by_PRD'].widget.attrs.update({
            'name': 'fixed_equip_protected'
        })
        self.fields['Protected_Equipment_Demage_Status'].widget.attrs.update({
            'name': 'protected_equip_demage'
        })
        self.fields['Fixed_Equipment_Protected_by_PRD'].required = False
        self.fields['Protected_Equipment_Demage_Status'].required = False
        self.fields['Maximum_Allow_able_Working_Pressure_of_Protected_Equipment'].required = False
        self.fields['Operating_Pressure_of_the_Protected_Equipment'].required = False

    class Meta:
        model = ProtectedFixedEquipmentPipingData
        fields = ['Fixed_Equipment_Protected_by_PRD',
                  'Protected_Equipment_Demage_Status',
                  'Maximum_Allow_able_Working_Pressure_of_Protected_Equipment',
                  'Operating_Pressure_of_the_Protected_Equipment',
                  'management_system_factor']


class ConsequencesOfFailureInputDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsequencesOfFailureInputDataForm, self).__init__(*args, **kwargs)
        self.fields['Multiple_PRDs_protecting_fixed_equipment'].required = False
        self.fields['Orifice_area_of_the_PRD'].required = False
        self.fields['Total_installed_orifice_area_of_a_multiple_PDRs_installation'].required = False


    class Meta:
        model = ConsequencesOfFailureInputData
        fields = ['Multiple_PRDs_protecting_fixed_equipment',
                  'Orifice_area_of_the_PRD',
                  'Total_installed_orifice_area_of_a_multiple_PDRs_installation']


class Consequences0fFailureOfLeakageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Consequences0fFailureOfLeakageForm, self).__init__(*args, **kwargs)
        self.fields['Rated_Capacity_of_PRD'].required = False
        self.fields['PRD_Inlet_Size'].required = False
        self.fields['Cost_of_the_fluid'].required = False
        self.fields['Environmental_clean_up_costs_due_to_a_PRD_leakage'].required = False
        self.fields['PRD_leakage_can_be_tolered'].required = False
        self.fields['Cost_of_shutdown_to_repair_PRD'].required = False
        self.fields['Daily_production_margin_on_the_unit'].required = False
        self.fields['Days_required_to_shutdown_a_unit_to_repair_a_leakage'].required = False

    class Meta:
        model = Consequences0fFailureOfLeakage
        fields = ['Rated_Capacity_of_PRD',
                  'PRD_Inlet_Size',
                  'Cost_of_the_fluid',
                  'Environmental_clean_up_costs_due_to_a_PRD_leakage',
                  'PRD_leakage_can_be_tolered',
                  'Cost_of_shutdown_to_repair_PRD',
                  'Daily_production_margin_on_the_unit',
                  'Days_required_to_shutdown_a_unit_to_repair_a_leakage']


class ApplicableOverpressureDemandCaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicableOverpressureDemandCaseForm, self).__init__(*args, **kwargs)
        self.fields['Over_pressure_demand_case'].required = False
        self.fields['Overpressure_associated_with_the_overpressure'].required = False
        self.fields['PRD_COF_to_open_associated_with_jth_overpressure'].required = False

    class Meta:
        model = ApplicableOverpressureDemandCase
        fields = ['Over_pressure_demand_case',
                  'Overpressure_associated_with_the_overpressure',
                  'PRD_COF_to_open_associated_with_jth_overpressure']



class Prd_InspectionHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Prd_InspectionHistoryForm, self).__init__(*args, **kwargs)
        self.fields['RBI_inspection_test_date'].required = False
        self.fields['PRD_pop_test_results'].required = False
        self.fields['PRD_Leakage_results'].required = False
        self.fields['PRD_Inspection_Effectiveness'].required = False
        self.fields['PRD_Overhauled_during_the_inspection'].required = False
        self.fields['PRD_replace_with_new_PRD_in_lieu_of_overhaul'].required = False


    class Meta:
        widgets = {
            'RBI_inspection_test_date': DateInput()
        }
        model = Prd_InspectionHistory
        fields = ['RBI_inspection_test_date',
                  'PRD_pop_test_results',
                  'PRD_Leakage_results',
                  'PRD_Inspection_Effectiveness',
                  'PRD_Overhauled_during_the_inspection',
                  'PRD_replace_with_new_PRD_in_lieu_of_overhaul']
