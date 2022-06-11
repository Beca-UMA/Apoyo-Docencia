from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Classroom
# Register your models here.

admin.site.register(Classroom)

class ClassroomAdmin(ImportExportModelAdmin):
    list_display = ('num_class', 'specification', 'location', 'num_pc',
                    's_o', 'capacity', 'specialization')
