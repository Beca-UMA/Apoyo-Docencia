# Generated by Django 4.0.4 on 2022-07-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('num_class', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('specification', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=150)),
                ('num_pc', models.BigIntegerField(default=0)),
                ('s_o', models.CharField(max_length=20)),
                ('capacity', models.CharField(max_length=20)),
                ('specialization', models.CharField(max_length=100)),
            ],
        ),
    ]
