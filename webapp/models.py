from django.db import models
from datetime import datetime
from django import forms
from django.utils import timezone
import json
from .IPRD_INPUT_CHOICES import *


degree_sign = u"\N{DEGREE SIGN}"


class TypeOfPRD(models.Model):
    Type_of_PRD = models.CharField(max_length=25,
                                   choices=IPRD_3_CHOICES,
                                   default='convention_spring_loaded')
                                   
    def __str__(self):
        return self.Type_of_PRD


class ServiceSeverity(models.Model):
    Service_severity = models.CharField(max_length=15,
                       choices=IPRD_6_CHOICES,
                       default='mild')
                       
    def __str__(self):
        return self.Service_severity
       


class PRDDischargeLocation(models.Model):
    PRD_Discharge_Location = models.CharField(max_length=25,
                             choices=IPRD_7_CHOICES,
                             default='atmosphere')
                             
    def __str__(self):
        return self.PRD_Discharge_Location


class EnvironmentFactorModifier(models.Model):
    Environment_Factor_Modifier = models.CharField(max_length=100,
                            choices=IPRD_8_CHOICES,
                            default=f'99.33 {degree_sign}C < T < 260 {degree_sign}C')
                            
    def __str__(self):
        return self.Environment_Factor_Modifier



class ProtectedEquipmentDemageStatus(models.Model):
    Protected_Equipment_Demage_Status = models.CharField(max_length=15,
                            choices=IPRD_19_CHOICES,
                            default='none')
                            
    def __str__(self):
        return self.Protected_Equipment_Demage_Status


class PRDInspectionEffectiveness(models.Model):
    PRD_Inspection_Effectiveness = models.CharField(max_length=30,
                            choices=IPRD_13_CHOICES,
                            default='highly_effective')
                            
    def __str__(self):
        return self.PRD_Inspection_Effectiveness


class OverPressureDemandCase(models.Model):
    Over_pressure_demand_case = models.CharField(max_length=100,
                            choices=IPRD_16_CHOICES,
                            default='fire')
                            
    def __str__(self):
        return self.Over_pressure_demand_case


class SelectField(models.Model):
    Type_of_PRD = models.ForeignKey(TypeOfPRD,
                            on_delete=models.CASCADE)
    Service_severity = models.ForeignKey(ServiceSeverity,
                            on_delete=models.CASCADE)
    PRD_Discharge_Location = models.ForeignKey(PRDDischargeLocation,
                            on_delete=models.CASCADE)
    Environment_Factor_Modifier = models.ForeignKey(EnvironmentFactorModifier,
                            on_delete=models.CASCADE)
    ProtectedEquipmentDemageStatus = models.ForeignKey(ProtectedEquipmentDemageStatus,
                            on_delete=models.CASCADE,
                            default='')
    PRDInspectionEffectiveness = models.ForeignKey(PRDInspectionEffectiveness,
                            on_delete=models.CASCADE,
                            default='')
    OverPressureDemandCase = models.ForeignKey(OverPressureDemandCase,
                            on_delete=models.CASCADE,
                            default='')





class GeneralInformationQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "PRD_identification_number", 
                                       "PRD_function",
                                       "Installation_of_PRD",
                                       "RBI_assessment_date",
                                       "Type_of_PRD",
                                       "PRD_Containing_Soft_Seats",
                                       "PRD_set",
                                       "Service_severity",
                                       "PRD_Discharge_Location",
                                       "Environment_Factor_Modifier",
                                       "Rupture_disk_is_installed_upstream_of_PRD"))

        #list_values[0]['model'] = self.model._meta.model_nam
        #self.model._meta.model_nam
        return list_values



class GeneralInformationManager(models.Manager):
    def get_queryset(self):
        return GeneralInformationQuerySet(self.model, using=self._db)



class GeneralInformation(models.Model):
    PRD_identification_number = models.CharField(max_length=10)
    PRD_function = models.CharField(max_length=150)
    Installation_of_PRD = models.DateField(default=datetime.now)
    RBI_assessment_date = models.DateField(default=datetime.now)
    Type_of_PRD = models.CharField(max_length=25,
                                   choices=IPRD_3_CHOICES,
                                   default='convention_spring_loaded')
    PRD_Containing_Soft_Seats = models.CharField(
                max_length=15,
                choices=IPRD_4_CHOICES,
                default='no')
    PRD_set = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  default=1.0)
    Service_severity = models.CharField(max_length=15,
                       choices=IPRD_6_CHOICES,
                       default='mild')
    PRD_Discharge_Location = models.CharField(max_length=25,
                             choices=IPRD_7_CHOICES,
                             default='atmosphere')
    Environment_Factor_Modifier = models.CharField(max_length=100,
                            choices=IPRD_8_CHOICES,
                            default=f'99.33 {degree_sign}C < T < 260 {degree_sign}C')
    Rupture_disk_is_installed_upstream_of_PRD = models.CharField(max_length=13,
                            choices=IPRD_9_CHOICES,
                            default='no')
                            
    objects = GeneralInformationManager()
    
    
    class Meta:
        ordering = ['id',]

    def __str__(self):
        return f'{self.PRD_identification_number}'
        
        
    def serialize(self):
        data = {
            "id": self.id,
            "PRD_identification_number": self.PRD_identification_number,
            "PRD_function": self.PRD_function,
            "Installation_of_PRD": self.Installation_of_PRD,
            "RBI_assessment_date": self.RBI_assessment_date
        }
        data = json.dumps(data)
        return data
        
        
        
    
class PrdInspection_TestHistoryQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "Fixed_Equipment_Protected_by_PRD", 
                                       "Protected_Equipment_Demage_Status",
                                       "Maximum_Allow_able_Working_Pressure_of_Protected_Equipment",
                                       "Operating_Pressure_of_the_Protected_Equipment",
                                       "management_system_factor",
                                       "management_system_factor"))

        return list_values



class PrdInspection_TestHistoryManager(models.Manager):
    def get_queryset(self):
        return PrdInspection_TestHistoryQuerySet(self.model, using=self._db)
        


class PrdInspection_TestHistory(models.Model):
    Fixed_Equipment_Protected_by_PRD = models.CharField(max_length=20,
                            choices=IPRD_18_CHOICES,
                            default='yes')
    Protected_Equipment_Demage_Status = models.CharField(max_length=15,
                            choices=IPRD_19_CHOICES,
                            default='none')
    Maximum_Allow_able_Working_Pressure_of_Protected_Equipment = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Operating_Pressure_of_the_Protected_Equipment = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    management_system_factor = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    
    objects = PrdInspection_TestHistoryManager()


    class Meta:
        ordering = ['id']


    def __str__(self):
        return f'{self.Fixed_Equipment_Protected_by_PRD}'
        
    
    def serialize(self):
        data = {
            "id": self.id,
            "Fixed_Equipment_Protected_by_PRD": self.Fixed_Equipment_Protected_by_PRD,
            "Protected_Equipment_Demage_Status": self.Protected_Equipment_Demage_Status,
            "Maximum_Allow_able_Working_Pressure_of_Protected_Equipment": self.Maximum_Allow_able_Working_Pressure_of_Protected_Equipment,
            "Operating_Pressure_of_the_Protected_Equipment": self.Operating_Pressure_of_the_Protected_Equipment,
            "management_system_factor": self.management_system_factor,
        }
        data = json.dumps(data)
        return data





class ConsequencesOfFailureInputDataQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "Multiple_PRDs_protecting_fixed_equipment", 
                                       "Orifice_area_of_the_PRD",
                                       "Total_installed_orifice_area_of_a_multiple_PDRs_installation"))

        return list_values



class ConsequencesOfFailureInputDataManager(models.Manager):
    def get_queryset(self):
        return ConsequencesOfFailureInputDataQuerySet(self.model, using=self._db)



class ConsequencesOfFailureInputData(models.Model):
    Multiple_PRDs_protecting_fixed_equipment = models.CharField(max_length=14,
                            choices=IPRD_22_CHOICES,
                            default='yes')
    Orifice_area_of_the_PRD = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Total_installed_orifice_area_of_a_multiple_PDRs_installation = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
                            
    objects = ConsequencesOfFailureInputDataManager()

    class Meta:
        ordering = ['id']


    def __str__(self):
        return f'{self.Multiple_PRDs_protecting_fixed_equipment}'
        
    
    def serialize(self):
        data = {
            "id": self.id,
            "Multiple_PRDs_protecting_fixed_equipment": self.Multiple_PRDs_protecting_fixed_equipment,
            "Orifice_area_of_the_PRD": self.Orifice_area_of_the_PRD,
            "Total_installed_orifice_area_of_a_multiple_PDRs_installation": self.Total_installed_orifice_area_of_a_multiple_PDRs_installation,
        }
        data = json.dumps(data)
        return data




class Consequences0fFailureOfLeakageQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "Rated_Capacity_of_PRD", 
                                       "PRD_Inlet_Size",
                                       "Cost_of_the_fluid",
                                       "Environmental_clean_up_costs_due_to_a_PRD_leakage",
                                       "PRD_leakage_can_be_tolered",
                                       "Cost_of_shutdown_to_repair_PRD",
                                       "Daily_production_margin_on_the_unit",
                                       "Days_required_to_shutdown_a_unit_to_repair_a_leakage"))

        return list_values



class Consequences0fFailureOfLeakageManager(models.Manager):
    def get_queryset(self):
        return Consequences0fFailureOfLeakageQuerySet(self.model, using=self._db)



class Consequences0fFailureOfLeakage(models.Model):
    Rated_Capacity_of_PRD = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    PRD_Inlet_Size = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Cost_of_the_fluid = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Environmental_clean_up_costs_due_to_a_PRD_leakage = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    PRD_leakage_can_be_tolered = models.CharField(max_length=14,
                            choices=IPRD_30_CHOICES,
                            default='no')
    Cost_of_shutdown_to_repair_PRD = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Daily_production_margin_on_the_unit = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    Days_required_to_shutdown_a_unit_to_repair_a_leakage = models.DecimalField(max_digits=10,
                            decimal_places=3,
                            default=1.0)
                            
    objects = Consequences0fFailureOfLeakageManager()
                            
    def __str__(self):
        return f'{self.Rated_Capacity_of_PRD}'
        
        
    class Meta:
        ordering = ['id']
        
        
    def serialize(self):
        data = {
            "id": self.id,
            "Rated_Capacity_of_PRD": self.Rated_Capacity_of_PRD,
            "PRD_Inlet_Size": self.PRD_Inlet_Size,
            "Cost_of_the_fluid": self.Cost_of_the_fluid,
            "Environmental_clean_up_costs_due_to_a_PRD_leakage": self.Environmental_clean_up_costs_due_to_a_PRD_leakage,
            "PRD_leakage_can_be_tolered": self.PRD_leakage_can_be_tolered,
            "Cost_of_shutdown_to_repair_PRD": self.Cost_of_shutdown_to_repair_PRD,
            "Daily_production_margin_on_the_unit": self.Daily_production_margin_on_the_unit
        }
        data = json.dumps(data)
        return data



class Prd_InspectionHistoryQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "RBI_inspection_test_date", 
                                       "PRD_pop_test_results",
                                       "PRD_Leakage_results",
                                       "PRD_Inspection_Effectiveness",
                                       "PRD_Overhauled_during_the_inspection",
                                       "PRD_replace_with_new_PRD_in_lieu_of_overhaul"))

        return list_values



class Prd_InspectionHistorygeManager(models.Manager):
    def get_queryset(self):
        return Prd_InspectionHistoryQuerySet(self.model, using=self._db)


class Prd_InspectionHistory(models.Model):
    RBI_inspection_test_date = models.DateField(blank=True, null=True)
    PRD_pop_test_results = models.CharField(max_length=15,
                            choices=IPRD_11_CHOICES,
                            default='fire')
    PRD_Leakage_results = models.CharField(max_length=15,
                            choices=IPRD_12_CHOICES,
                            default='pass')
    PRD_Inspection_Effectiveness = models.CharField(max_length=30,
                            choices=IPRD_13_CHOICES,
                            default='highly_effective')
    PRD_Overhauled_during_the_inspection = models.CharField(max_length=14,
                            choices=IPRD_14_CHOICES,
                            default='yes')
    PRD_replace_with_new_PRD_in_lieu_of_overhaul = models.CharField(max_length=14,
                            choices=IPRD_15_CHOICES,
                            default='no')
                            
    objects = Prd_InspectionHistorygeManager()
    
    def __str__(self):
        return f'{self.RBI_inspection_test_date}'
        
    
    class Meta:
        ordering = ['id']
        
    
    def serialize(self):
        data = {
            "id": self.id,
            "RBI_inspection_test_date": self.RBI_inspection_test_date,
            "PRD_pop_test_results": self.PRD_pop_test_results,
            "PRD_Leakage_results": self.PRD_Leakage_results,
            "PRD_Inspection_Effectiveness": self.PRD_Inspection_Effectiveness,
            "PRD_Overhauled_during_the_inspection": self.PRD_Overhauled_during_the_inspection,
            "PRD_replace_with_new_PRD_in_lieu_of_overhaul": self.PRD_replace_with_new_PRD_in_lieu_of_overhaul,
        }
        data = json.dumps(data)
        return data




class ApplicableOverpressureDemandCaseQuerySet(models.QuerySet):         
    def serialize(self):
        list_values = list(self.values("id", "Over_pressure_demand_case", 
                                       "Overpressure_associated_with_the_overpressure",
                                       "PRD_COF_to_open_associated_with_jth_overpressure"))

        return list_values



class ApplicableOverpressureDemandCaseManager(models.Manager):
    def get_queryset(self):
        return ApplicableOverpressureDemandCaseQuerySet(self.model, using=self._db)




class ApplicableOverpressureDemandCase(models.Model):
    Over_pressure_demand_case = models.CharField(max_length=100,
                            choices=IPRD_16_CHOICES,
                            default='fire')
    Overpressure_associated_with_the_overpressure = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    PRD_COF_to_open_associated_with_jth_overpressure = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=1.0)
    
    objects = ApplicableOverpressureDemandCaseManager()
    
    def __str__(self):
        return f'{self.Over_pressure_demand_case}'
        
        
    class Meta:
        ordering = ['id']
        
        
    def serialize(self):
        data = {
            "id": self.id,
            "Over_pressure_demand_case": self.Over_pressure_demand_case,
            "Overpressure_associated_with_the_overpressure": self.Overpressure_associated_with_the_overpressure,
            "PRD_COF_to_open_associated_with_jth_overpressure": self.PRD_COF_to_open_associated_with_jth_overpressure
        }
        data = json.dumps(data)
        return data
        