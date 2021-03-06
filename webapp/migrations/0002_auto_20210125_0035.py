# Generated by Django 3.1.4 on 2021-01-25 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prdinspection_testhistory',
            name='Protected_Equipment_Demage_Status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.protectedequipmentdemagestatus'),
        ),
        migrations.AlterField(
            model_name='protectedequipmentdemagestatus',
            name='name',
            field=models.CharField(choices=[('none', 'None'), ('minimal', 'Minimal'), ('minor', 'Minor'), ('moderate', 'Moderate'), ('severe', 'Severe')], default='none', max_length=15),
        ),
    ]
