from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('newRequest/', views.newRequestClass),
    path('showRequest/<key>', views.showRequest),
    path('createRequest/', views.createRequestClass),
    path('removeRequest/<key>', views.removeRequest),
    path('editRequest/<key>', views.editRequest),
    path('editRequest/updateRequest/', views.updateRequest),
    path('', views.importRequest)
] 