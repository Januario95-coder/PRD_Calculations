# Generated by Django 3.1.1 on 2020-10-09 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0033_auto_20201009_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinformation',
            name='Installation_of_PRD',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='generalinformation',
            name='RBI_assessment_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
