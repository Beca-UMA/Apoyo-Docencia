from pyexpat import model
from django.db import models
import uuid 


# Create your models here.
class Period(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the period")
    year = models.DateField()
    typ = models.CharField(max_length=100, help_text="Cuatrimestre, examanes...")

    def __str__(self):
        return f"Año: {self.year}, tipo de periodo: {self.typ}"
    
    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)

    def __hash__(self) -> int:
        return super().__hash__()