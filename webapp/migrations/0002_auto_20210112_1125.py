# Generated by Django 3.1.4 on 2021-01-12 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consequencesoffailureinputdata',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='generalinformation',
            options={'ordering': ['id']},
        ),
    ]
