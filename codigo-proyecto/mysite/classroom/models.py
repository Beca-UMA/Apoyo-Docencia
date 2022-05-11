from django.db import models


class Classroom(models.Model):
    specification = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    num_pc = models.BigIntegerField(default=0)
    s_o = models.CharField(max_length=20)
    num_class = models.CharField(max_length=10)
    capacity = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)

