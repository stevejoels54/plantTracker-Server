from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .models import Reading, Notification
from .serializers import ReadingSerializer, NotificationSerializer
from .notifications import check_temperature, check_light, check_moisture
from datetime import datetime, timedelta

# Create your views here.


@csrf_exempt
def readings(request):
    if request.method == 'GET':
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReadingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# function that adds a new reading to the database through values passed in the url
@csrf_exempt
def add_reading(request, device_id, temperature, light, moisture):
    if request.method == 'POST':
        reading_time = request.GET.get(
            'reading_time')  # Get value from query parameter
        data = {
            'device_id': device_id,
            'temperature': temperature,
            'light': light,
            'moisture': moisture,
            'reading_time': reading_time,
        }

        # Call the notification functions
        check_temperature(device_id, temperature)
        check_light(device_id, light)
        check_moisture(device_id, moisture)

        serializer = ReadingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# function that returns the current reading for a device
@csrf_exempt
def current_reading(request, device_id):
    if request.method == 'GET':
        try:
            reading = Reading.objects.filter(
                device_id=device_id).latest('reading_time')
            serializer = ReadingSerializer(reading)
            return JsonResponse(serializer.data, safe=False)
        except Reading.DoesNotExist:
            return JsonResponse({'error': 'Reading not found'}, status=404)


@csrf_exempt
def reading_detail(request, pk):
    try:
        reading = Reading.objects.get(pk=pk)
    except Reading.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReadingSerializer(reading)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReadingSerializer(reading, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        reading.delete()
        return HttpResponse(status=204)


@csrf_exempt
def notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def notifications_by_device(request, device_id):
    if request.method == 'GET':
        notifications = Notification.objects.filter(
            device_id=device_id).order_by('-notification_time')
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)