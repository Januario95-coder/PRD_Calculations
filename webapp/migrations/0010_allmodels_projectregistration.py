# Generated by Django 3.1.4 on 2021-03-07 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20210307_0709'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRD_Inspection_history', models.ManyToManyField(to='webapp.Prd_InspectionHistory')),
                ('applicable_overpressure_demand', models.ManyToManyField(to='webapp.ApplicableOverpressureDemandCase')),
                ('consequence_of_failure_input_data', models.ManyToManyField(to='webapp.ConsequencesOfFailureInputData')),
                ('consequence_of_failure_leakage', models.ManyToManyField(to='webapp.ConsequencesOfFailureOfLeakage')),
                ('general_information', models.ManyToManyField(to='webapp.GeneralInformation')),
                ('protected_fixed_equip', models.ManyToManyField(to='webapp.ProtectedFixedEquipmentPipingData')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150)),
                ('project_function', models.CharField(max_length=150)),
                ('creation_date', models.DateField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.allmodels')),
            ],
        ),
    ]
