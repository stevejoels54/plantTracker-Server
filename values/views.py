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
from django.db.models import Avg
from django.utils import timezone
from django.conf import settings
import csv
from devices.models import Device

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
            device_id=device_id).order_by('-notification_time')[:9]
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
def get_summary(request, device_id):

    # Disable time zone support
    settings.USE_TZ = False

    # Filter out the daySummary data for the given device_id
    now = timezone.now()
    day_summary_data = Reading.objects.filter(device_id=device_id,
                                              reading_time__date=now.date())

    # Calculate morning, afternoon, and evening summaries for daySummary
    morning_summary = day_summary_data.filter(
        reading_time__time__range=("00:00", "11:59")).aggregate(
            temperature=Avg('temperature'),
            light=Avg('light'),
            moisture=Avg('moisture'))
    afternoon_summary = day_summary_data.filter(
        reading_time__time__range=("12:00", "17:59")).aggregate(
            temperature=Avg('temperature'),
            light=Avg('light'),
            moisture=Avg('moisture'))
    evening_summary = day_summary_data.filter(
        reading_time__time__range=("18:00", "23:59")).aggregate(
            temperature=Avg('temperature'),
            light=Avg('light'),
            moisture=Avg('moisture'))

    # Calculate weekSummary
    week_start_date = now.date() - timedelta(days=7)
    week_summary_data = Reading.objects.filter(
        device_id=device_id, reading_time__gte=week_start_date)
    week_summary = week_summary_data.aggregate(temperature=Avg('temperature'),
                                               light=Avg('light'),
                                               moisture=Avg('moisture'))

    # Calculate monthSummary
    month_start_date = now.date() - timedelta(days=30)
    month_summary_data = Reading.objects.filter(
        device_id=device_id, reading_time__gte=month_start_date)
    month_summary = month_summary_data.aggregate(
        temperature=Avg('temperature'),
        light=Avg('light'),
        moisture=Avg('moisture'))

    # Create the summary object with daySummary, weekSummary, and monthSummary
    summary = {
        'daySummary': {
            'morning': {
                'temperature': morning_summary['temperature'],
                'light': morning_summary['light'],
                'moisture': morning_summary['moisture'],
            },
            'afternoon': {
                'temperature': afternoon_summary['temperature'],
                'light': afternoon_summary['light'],
                'moisture': afternoon_summary['moisture'],
            },
            'evening': {
                'temperature': evening_summary['temperature'],
                'light': evening_summary['light'],
                'moisture': evening_summary['moisture'],
            },
        },
        'weekSummary': {
            'temperature': week_summary['temperature'],
            'light': week_summary['light'],
            'moisture': week_summary['moisture'],
        },
        'monthSummary': {
            'temperature': month_summary['temperature'],
            'light': month_summary['light'],
            'moisture': month_summary['moisture'],
        },
    }

    # Return the summary object as a JSON response
    return JsonResponse(summary)


@csrf_exempt
def export_data(request, device_id):
    # Retrieve data from the Reading model for the given device_id
    device_data = Reading.objects.filter(device_id=device_id)

    # Create the HttpResponse object with appropriate headers for a CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="device_data.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow([
        'reading_id', 'device_id', 'reading_time', 'temperature', 'light',
        'moisture'
    ])

    # Write data rows to the CSV file
    for data in device_data:
        writer.writerow([
            data.reading_id, data.device_id.device_id, data.reading_time,
            data.temperature, data.light, data.moisture
        ])

    return response


@csrf_exempt
def device_data(request, device_id):
    # Retrieve the device object
    device = Device.objects.get(device_id=device_id)

    # Retrieve all the readings associated with the device and sort them by most recent
    readings = Reading.objects.filter(
        device_id=device).order_by('-reading_time')

    # Render the data in a template
    context = {'device': device, 'readings': readings}
    return render(request, 'device_data.html', context)