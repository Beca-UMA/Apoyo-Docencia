from django.db import models
import uuid 
from Aplicaciones.request_class.models import RequestClass
from Aplicaciones.classroom.models import Classroom

# Create your models here.
class Slot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the slot")
    day = models.DateField()
    schedule = models.DateField()
    request = models.ForeignKey(RequestClass, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)



    def __str__(self) -> str:
        return f"Day: {self.day}, horario: {self.schedule}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Slot):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.day == other.day and self.schedule == other.schedule

    def __hash__(self) -> int:
        return super().__hash__()