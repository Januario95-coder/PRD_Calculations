# Generated by Django 3.1.1 on 2020-10-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0041_auto_20201023_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinformation',
            name='PRD_identification_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='prd_inspectionhistory',
            name='PRD_Overhauled_during_the_inspection',
            field=models.CharField(choices=[('none', 'None'), ('yes', 'Yes'), ('no', 'No')], default='yes', max_length=14),
        ),
        migrations.AlterField(
            model_name='prd_inspectionhistory',
            name='PRD_replace_with_new_PRD_in_lieu_of_overhaul',
            field=models.CharField(choices=[('none', 'None'), ('yes', 'Yes'), ('no', 'No')], default='no', max_length=14),
        ),
    ]
