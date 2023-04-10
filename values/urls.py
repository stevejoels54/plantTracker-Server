from django.urls import path
from . import views

urlpatterns = [
    path('readings', views.readings, name='readings'),
    path(
        'add_reading/<int:device_id>/<int:temperature>/<int:light>/<int:moisture>',
        views.add_reading,
        name='add_reading'),
    path('current_reading/<int:device_id>',
         views.current_reading,
         name='current_reading'),
    path('<int:pk>/', views.reading_detail, name='reading_detail'),
    path('notifications', views.notifications, name='notifications'),
    path('notifications_by_device/<int:device_id>',
         views.notifications_by_device,
         name='notifications_by_device')
]