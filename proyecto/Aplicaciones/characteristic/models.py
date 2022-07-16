from django.db import models
import uuid

from Aplicaciones.request_class.models import RequestClass 
from Aplicaciones.classroom.models import Classroom 


# Create your models here.
class Characteristic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the characteristic")
    name = models.CharField(max_length=100)
    numeric = models.BooleanField()
    applicnat = models.ForeignKey(RequestClass, null= True,  on_delete=models.PROTECT)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
