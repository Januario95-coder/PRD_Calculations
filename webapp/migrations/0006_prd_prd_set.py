# Generated by Django 3.1.1 on 2020-09-22 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_prd_prd_containing_soft_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='prd',
            name='PRD_set',
            field=models.DecimalField(decimal_places=3, default=1.0, max_digits=10),
        ),
    ]