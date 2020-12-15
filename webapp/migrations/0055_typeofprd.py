# Generated by Django 3.1.1 on 2020-12-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0054_auto_20201128_0158'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOfPRD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type_of_PRD', models.CharField(choices=[('convention_spring_loaded', 'Convention Spring-Loaded'), ('balanced_bellows', 'Balanced Bellows'), ('pilot_operated', 'Pilot Operated'), ('Rupture_disk_only', 'Rupture Disk Only')], default='convention_spring_loaded', max_length=25)),
            ],
        ),
    ]
