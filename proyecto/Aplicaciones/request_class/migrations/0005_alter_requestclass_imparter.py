# Generated by Django 4.0.4 on 2022-07-15 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
        ('request_class', '0004_rename_id_requestclass_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestclass',
            name='imparter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_teacher', to='teacher.teacher'),
        ),
    ]
