from django.db import models
import uuid 


# Create your models here.
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the teacher")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)
    email = models.CharField(max_length=40)
    department = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.name}"


    def __eq__(self, other):
        if not isinstance(other, Teacher):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.id == other.id

    
    def __hash__(self) -> int:
        return super().__hash__()
