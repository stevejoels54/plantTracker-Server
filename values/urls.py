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
         name='notifications_by_device'),
    path('summary/<int:device_id>', views.get_summary, name='summary'),
    path('export/<int:device_id>/', views.export_data, name='export_data'),
    path('device_data/<int:device_id>/', views.device_data,
         name='device_data'),
]