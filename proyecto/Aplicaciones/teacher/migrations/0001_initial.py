# Generated by Django 4.0.6 on 2022-08-17 10:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID unique for the teacher', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=9)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('department', models.CharField(max_length=100)),
            ],
        ),
    ]
