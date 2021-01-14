# Generated by Django 3.1.4 on 2021-01-14 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210114_1417'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApplicableOverpressureDemandCase',
        ),
        migrations.DeleteModel(
            name='Consequences0fFailureOfLeakage',
        ),
        migrations.DeleteModel(
            name='ConsequencesOfFailureInputData',
        ),
        migrations.DeleteModel(
            name='GeneralInformation',
        ),
        migrations.DeleteModel(
            name='Prd_InspectionHistory',
        ),
        migrations.DeleteModel(
            name='PrdInspection_TestHistory',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='Environment_Factor_Modifier',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='OverPressureDemandCase',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='PRDInspectionEffectiveness',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='PRD_Discharge_Location',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='ProtectedEquipmentDemageStatus',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='Service_severity',
        ),
        migrations.RemoveField(
            model_name='selectfield',
            name='Type_of_PRD',
        ),
        migrations.DeleteModel(
            name='EnvironmentFactorModifier',
        ),
        migrations.DeleteModel(
            name='OverPressureDemandCase',
        ),
        migrations.DeleteModel(
            name='PRDDischargeLocation',
        ),
        migrations.DeleteModel(
            name='PRDInspectionEffectiveness',
        ),
        migrations.DeleteModel(
            name='ProtectedEquipmentDemageStatus',
        ),
        migrations.DeleteModel(
            name='SelectField',
        ),
        migrations.DeleteModel(
            name='ServiceSeverity',
        ),
        migrations.DeleteModel(
            name='TypeOfPRD',
        ),
    ]