from django.contrib import admin
from django.core.serializers import serialize
from django.http import HttpResponse
from webapp.models import (
    # TypeOfPRD,
    # ServiceSeverity,
    # PRDDischargeLocation,
    # EnvironmentFactorModifier,
    # ProtectedEquipmentDemageStatus,
    # PRDInspectionEffectiveness,
    # OverPressureDemandCase,

    # SelectField,

    GeneralInformation,
    PrdInspection_TestHistory,
    ConsequencesOfFailureInputData,
    Consequences0fFailureOfLeakage,
    ApplicableOverpressureDemandCase,
    Prd_InspectionHistory
)
import csv
import datetime



def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        f'filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields()
              if not field.many_to_many
              and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = "Export to CSV"


# def export_as_json(modeladmin, request, queryset):
#     response = HttpResponse(content_type='application/json')
#     serialize('json', queryset, stream=response)
#     return response


# export_as_json.short_description = "Export as JSON"


# @admin.register(TypeOfPRD)
# class TypeOfPRDAdmin(admin.ModelAdmin):
#     list_display = ['Type_of_PRD']


# @admin.register(ServiceSeverity)
# class ServiceSeverityAdmin(admin.ModelAdmin):
#     list_display = ['Service_severity']

# @admin.register(PRDDischargeLocation)
# class PRDDischargeLocationAdmin(admin.ModelAdmin):
#     list_display = ['PRD_Discharge_Location']

# @admin.register(EnvironmentFactorModifier)
# class EnvironmentFactorModifierAdmin(admin.ModelAdmin):
#     list_display = ['Environment_Factor_Modifier']

# @admin.register(ProtectedEquipmentDemageStatus)
# class ProtectedEquipmentDemageStatusAdmin(admin.ModelAdmin):
#     list_display = ['Protected_Equipment_Demage_Status']

# @admin.register(PRDInspectionEffectiveness)
# class PRDInspectionEffectivenessAdmin(admin.ModelAdmin):
#     list_display = ['PRD_Inspection_Effectiveness']

# @admin.register(OverPressureDemandCase)
# class OverPressureDemandCaseAdmin(admin.ModelAdmin):
#     list_display = ['Over_pressure_demand_case']



# @admin.register(SelectField)
# class SelectFieldAdmin(admin.ModelAdmin):
#     list_display = ['Type_of_PRD',
#                     'Service_severity',
#                     'PRD_Discharge_Location',
#                     'Environment_Factor_Modifier']




@admin.register(GeneralInformation)
class PRDAdmin(admin.ModelAdmin):
    list_display = ['id', 'PRD_identification_number', 'PRD_function',
                    'Installation_of_PRD', 'RBI_assessment_date',
                    'Type_of_PRD', 'PRD_Containing_Soft_Seats',
                    'PRD_set', 'Service_severity',
                    'PRD_Discharge_Location', 'Environment_Factor_Modifier',
                    'Rupture_disk_is_installed_upstream_of_PRD']
    list_filter = ['PRD_identification_number',
                   'Type_of_PRD']
    actions = [export_to_csv, 'export_as_json']


    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        serialize('json', queryset, stream=response)
        return response

    export_as_json.short_description = "Export as JSON"



@admin.register(PrdInspection_TestHistory)
class PrdInspectionHistory(admin.ModelAdmin):
    list_display = ['id', 'Fixed_Equipment_Protected_by_PRD',
                    'Protected_Equipment_Demage_Status']


@admin.register(ConsequencesOfFailureInputData)
class ConsequencesOfFailureInputData(admin.ModelAdmin):
    list_display = ['Multiple_PRDs_protecting_fixed_equipment']


@admin.register(Consequences0fFailureOfLeakage)
class Consequences0fFailureOfLeakage(admin.ModelAdmin):
    list_display = ['id', 'Rated_Capacity_of_PRD',
                    'PRD_Inlet_Size',
                    'Cost_of_the_fluid',
                    'Environmental_clean_up_costs_due_to_a_PRD_leakage']


@admin.register(ApplicableOverpressureDemandCase)
class ApplicableOverpressureDemandCase(admin.ModelAdmin):
    list_display = ['id', 'Over_pressure_demand_case',
                 'Overpressure_associated_with_the_overpressure',
                 'PRD_COF_to_open_associated_with_jth_overpressure']


@admin.register(Prd_InspectionHistory)
class Prd_InspectionHistory(admin.ModelAdmin):
    list_display = ['id', 'RBI_inspection_test_date',
                    'PRD_pop_test_results',
                    'PRD_Leakage_results',
                    'PRD_Inspection_Effectiveness',
                    'PRD_Overhauled_during_the_inspection',
                    'PRD_replace_with_new_PRD_in_lieu_of_overhaul']
    list_editable = ['RBI_inspection_test_date',
                    'PRD_pop_test_results',
                    'PRD_Leakage_results',
                    'PRD_Inspection_Effectiveness',
                    'PRD_Overhauled_during_the_inspection',
                    'PRD_replace_with_new_PRD_in_lieu_of_overhaul']
