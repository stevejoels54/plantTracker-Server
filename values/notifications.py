from .models import Notification
from devices.models import Device
from django.utils import timezone


def create_notification(device, notification_type, notification_message):
    device = Device.objects.get(device_id=device)
    notification = Notification(device_id=device,
                                notification_time=timezone.now(),
                                notification_type=notification_type,
                                notification_message=notification_message)
    notification.save()


def check_temperature(device, temperature):
    if temperature > 30:
        create_notification(device, 'High temperature',
                            'Temperature is too high')
    elif temperature >= 20:
        create_notification(device, 'Moderate temperature',
                            'Temperature is at a moderate level')
    elif temperature >= 10:
        create_notification(device, 'Low temperature',
                            'Temperature is at a low level')
    else:
        create_notification(device, 'Normal temperature',
                            'Temperature is at a normal level')


def check_light(device, light):
    if light > 20000:
        create_notification(device, 'High light', 'Light is too high')
    elif light >= 5000:
        create_notification(device, 'Moderate light',
                            'Light is at a moderate level')
    elif light >= 1000:
        create_notification(device, 'Low light', 'Light is at a low level')
    else:
        create_notification(device, 'Normal light',
                            'Light is at a normal level')


def check_moisture(device, moisture):
    if moisture > 70:
        create_notification(device, 'Saturated moisture',
                            'Moisture is saturated')
    elif moisture >= 30:
        create_notification(device, 'Wet moisture',
                            'Moisture is at a wet level')
    elif moisture >= 10:
        create_notification(device, 'Moist moisture',
                            'Moisture is at a moist level')
    else:
        create_notification(device, 'Dry moisture',
                            'Moisture is at a dry level')
