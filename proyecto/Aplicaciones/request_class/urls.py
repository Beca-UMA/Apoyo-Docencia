from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('newRequest/', views.newRequestClass),
    path('createRequest/', views.createRequestClass),
    path('removeRequest/<key>', views.removeRequest),
    path('editRequest/<key>', views.editRequest),
    path('updateRequest/', views.updateRequest),
    path('', views.importRequest)
] 