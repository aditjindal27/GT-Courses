from django.urls import path
from . import views

urlpatterns = [
   path('info', views.home, name="home"),
   path('getInfo', views.getInfo, name="getInfo"),  
]
