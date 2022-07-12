from django.db import models
import uuid 

# Create your models here.
class SmallGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the small group")
    subject = models.CharField(max_length=100)
    grade =  models.IntegerField(default=5)
    letter = models.CharField(max_length=1)
    code = models.CharField(max_length=4)
    degree= models.CharField(max_length=100)

    def __str__(self):
        return self.code

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SmallGroup):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.subject == other.subject and self.code == other.code

    def __hash__(self) -> int:
        return super().__hash__()
