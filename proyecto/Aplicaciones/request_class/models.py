from django.db import models

from Aplicaciones.small_group.models import SmallGroup
from ..teacher.models import Teacher
from ..period.models import Period

import uuid 

# Create your models here.
class RequestClass(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the request")
    id = models.IntegerField(default=0000)
    typ =  models.CharField(max_length=100)
    preference = models.CharField(max_length=100)
    features =  models.CharField(max_length=100)
    localitation = models.CharField(max_length=150)
    speficication = models.CharField(max_length=100)
    num_alum = models.IntegerField(default=0)
    s_o = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_hour = models.DateField()
    end_hour = models.DateField()
    alternative_day = models.CharField(max_length=50)
    sender = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    small_group = models.ForeignKey(SmallGroup, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.id} Tipo: {self.typ}, Preferencia: {self.preference}"

    def __eq__(self, other):
        if not isinstance(other, RequestClass):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.key == other.key
    
    def __hash__(self):
        return hash(self.key, self.id, self.typ, self.preference, self.features,
                    self.localitation, self.speficication, self.num_alum,
                    self.s_o, self.specialization, self.start_date, self.end_date,
                    self.start_hour, self.end_hour, self.alternative_day)




