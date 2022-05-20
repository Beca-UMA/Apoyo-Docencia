from django.db import models
from django.core.files import File
import csv

# Create your models here.
class Classroom(models.Model):
    num_class = models.CharField(primary_key=True, max_length=10)
    specification = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    num_pc = models.BigIntegerField(default=0)
    s_o = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.location, self.num_class)

    def __eq__(self, other): 
        if not isinstance(other, Classroom):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.num_class == other.num_class and self.location == other.location