# Generated by Django 4.2.2 on 2023-06-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InSwitch', models.CharField(max_length=50)),
                ('CallingNumber', models.CharField(max_length=50)),
                ('CalledNumber', models.CharField(max_length=50)),
                ('CallDate', models.CharField(max_length=150)),
                ('CallHour', models.IntegerField(null=True)),
                ('CallMinute', models.IntegerField(null=True)),
                ('CallSecond', models.IntegerField()),
                ('CallDuration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Telecom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InSwitch', models.CharField(max_length=50)),
                ('CallingNumber', models.CharField(max_length=50)),
                ('CalledNumber', models.CharField(max_length=50)),
                ('CallDate', models.CharField(max_length=150)),
                ('CallHour', models.IntegerField(null=True)),
                ('CallMinute', models.IntegerField(null=True)),
                ('CallSecond', models.IntegerField()),
                ('CallDuration', models.IntegerField()),
            ],
        ),
    ]
