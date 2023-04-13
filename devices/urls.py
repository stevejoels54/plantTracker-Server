from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('devices', views.devices, name='devices'),
    path('<int:pk>/', views.device_detail, name='device_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)