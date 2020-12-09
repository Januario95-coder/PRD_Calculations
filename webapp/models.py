from django.db import models
from datetime import datetime
from django import forms
from django.utils import timezone
from .IPRD_INPUT_CHOICES import *


degree_sign = u"\N{DEGREE SIGN}"

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

    class Meta:
        ordering = ['PRD_identification_number',]

    def __str__(self):
        return f'{self.PRD_identification_number}'


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


    class Meta:
        ordering = ['Fixed_Equipment_Protected_by_PRD']


    def __str__(self):
        return f'{self.Fixed_Equipment_Protected_by_PRD}'


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

    class Meta:
        ordering = ['Multiple_PRDs_protecting_fixed_equipment']


    def __str__(self):
        return f'{self.Multiple_PRDs_protecting_fixed_equipment}'


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
