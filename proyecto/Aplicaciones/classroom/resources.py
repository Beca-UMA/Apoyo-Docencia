from import_export import resources
from .models import Classroom

class ClassromResource(resources.ModelResource):
    class meta:
        model = Classroom

