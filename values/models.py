from django.db import models
from devices.models import Device

# Create your models here.


class Reading(models.Model):
    reading_id = models.AutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    reading_time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    light = models.DecimalField(max_digits=5, decimal_places=2)
    moisture = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.reading_id


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    notification_time = models.DateTimeField()
    notification_type = models.CharField(max_length=50)
    notification_message = models.CharField(max_length=200)

    def __str__(self):
        return self.notification_id