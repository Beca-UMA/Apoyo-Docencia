from django.db import models

from Aplicaciones.small_group.models import SmallGroup
from ..teacher.models import Teacher
from ..period.models import Period

import uuid 

# Create your models here.
class RequestClass(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the request")
    code = models.IntegerField(default=0000)
    typ =  models.CharField(max_length=100)
    preference = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    specification = models.CharField(max_length=100)
    num_alum = models.IntegerField(default=0)
    s_o = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    alternative_day = models.CharField(max_length=50)
    sender = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=False, related_name='%(class)s_requests_sender')
    imparter = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name='%(class)s_requests_teacher')
    per = models.ForeignKey(Period, on_delete=models.CASCADE)
    s_g = models.ForeignKey(SmallGroup, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.key} Tipo: {self.typ}, Preferencia: {self.preference}"

    # def __eq__(self, other):
    #     if not isinstance(other, RequestClass):
    #         # don't attempt to compare against unrelated types
    #         return NotImplemented
    #     return self.id == other.ig and self.typ == other.typ and self.preference == other.preference
    
    # def __hash__(self):
    #     return hash(self.key, self.id, self.typ, self.preference,
    #                 self.location, self.specification, self.num_alum,
    #                 self.s_o, self.specialization, self.start_date, self.end_date,
    #                 self.start_hour, self.end_hour, self.alternative_day)




