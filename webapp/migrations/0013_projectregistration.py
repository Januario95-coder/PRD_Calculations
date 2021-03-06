# Generated by Django 3.1.4 on 2021-03-07 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_allmodels'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150)),
                ('project_function', models.CharField(max_length=150)),
                ('creation_date', models.DateField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.allmodels')),
            ],
        ),
    ]
