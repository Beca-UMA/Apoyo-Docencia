from django.db import models
import uuid 

# Create your models here.
class SmallGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unique for the small group")
    subject = models.CharField(max_length=100)
    grade =  models.IntegerField(default=5)
    letter = models.CharField(max_length=1)
    code = models.CharField(max_length=4)

    def __str__(self):
        return self.code

    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)

    def __hash__(self) -> int:
        return super().__hash__()
