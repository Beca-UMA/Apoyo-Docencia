from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('newClassroom/', views.newClassroom),
    path('createClassroom/', views.createClassroom),
    path('removeClassroom/<num_class>/<location>', views.removeClassroom),
    path('editClassroom/<num_class>/<location>', views.editClassroom),
    path('updateClassroom/', views.updateClassroom),

    path('importClassroom/', views.importClassroom)
] 