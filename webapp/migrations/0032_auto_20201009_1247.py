# Generated by Django 3.1.1 on 2020-10-09 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20200924_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalinformation',
            name='Installation_of_PRD',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='generalinformation',
            name='RBI_assessment_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]