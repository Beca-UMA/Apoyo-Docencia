# Generated by Django 4.0.6 on 2022-08-17 10:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
        ('request_class', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID unique for the characteristic', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('numeric', models.BooleanField()),
                ('applicnat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='request_class.requestclass')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
            ],
        ),
    ]
