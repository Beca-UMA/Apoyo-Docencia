from django.shortcuts import render
from Aplicaciones.slot.models import Slot
from proyecto.settings import BASE_DIR
import datetime
import traceback
import requests
import os
import json
import tempfile
import mimetypes
from django.http import HttpResponse

# Create your views here.
def index(request):
    slots = Slot.objects.all()
    return render(request, "index_slots.html", {"slots": slots})

