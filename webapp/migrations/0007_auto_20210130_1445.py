# Generated by Django 3.1.4 on 2021-01-30 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20210125_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinformation',
            name='Type_of_PRD',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gen_info', to='webapp.typeofprd'),
        ),
    ]