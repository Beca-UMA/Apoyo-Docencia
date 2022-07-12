from import_export import resources
from .models import RequestClass

class RequestClassResource(resources.ModelResource):
    class meta:
        model = RequestClass

