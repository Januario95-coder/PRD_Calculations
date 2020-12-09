# Generated by Django 3.1.1 on 2020-09-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20200922_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prd',
            name='Type_of_PRD',
            field=models.CharField(choices=[('IPRD_3_first', 'Convention Spring-Loaded'), ('IPRD_3_second', 'Balanced Bellows'), ('IPRD_3_third', 'Pilot Operated'), ('IPRD_3_fourth', 'PRV with Rupture Disk'), ('IPRD_3_fifth', 'Rupture Disk Only')], default='IPRD_3_second', max_length=25),
        ),
    ]