# Generated by Django 3.1.4 on 2021-01-25 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20210125_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicableoverpressuredemandcase',
            name='Over_pressure_demand_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.overpressuredemandcase'),
        ),
    ]
