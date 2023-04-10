from django.urls import path
from . import views

urlpatterns = [
    path('devices', views.devices, name='devices'),
    path('<int:pk>/', views.device_detail, name='device_detail'),
]