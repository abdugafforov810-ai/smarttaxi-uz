from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Driver, Order

import random
import json
import math


# =========================
# HOME PAGE
# =========================

def home(request):

    context = {

        'drivers_count': Driver.objects.count(),

        'online_count': Driver.objects.filter(
            online=True
        ).count(),

        'orders_count': Order.objects.count(),

    }

    return render(
        request,
        'index.html',
        context
    )


# =========================
# DRIVERS API
# =========================

def drivers_api(request):

    drivers = Driver.objects.all()

    data = []

    for driver in drivers:

        # 🚖 Live Taxi Movement
        if driver.online:

            driver.latitude += random.uniform(
                -0.001,
                0.001
            )

            driver.longitude += random.uniform(
                -0.001,
                0.001
            )

            driver.save()

        data.append({

            'id': driver.id,

            'name': driver.name,

            'car_number': driver.car_number,

            'phone': driver.phone,

            'car_model': driver.car_model,

            'rating': driver.rating,

            'photo': driver.photo,

            'lat': driver.latitude,

            'lng': driver.longitude,

            'status': driver.status,

            'online': driver.online,

        })

    return JsonResponse(
        data,
        safe=False
    )


# =========================
# ORDERS API
# =========================

def orders_api(request):

    orders = Order.objects.all().order_by(
        '-created_at'
    )

    data = []

    for order in orders:

        data.append({

            'id': order.id,

            'customer': order.customer_name,

            'from': order.from_location,

            'to': order.to_location,

            'status': order.status,

            'taxi_type': order.taxi_type,

            'passengers': order.passengers,

            'driver': (

                order.driver.name

                if order.driver

                else 'Driver topilmadi'

            )

        })

    return JsonResponse(
        data,
        safe=False
    )


# =========================
# CREATE ORDER
# =========================

@csrf_exempt
def create_order(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        nearest_driver = None

        min_distance = 999999

        drivers = Driver.objects.filter(
            status='online',
            online=True
        )

        # 🤖 AI Taxi Tanlash

        for driver in drivers:

            distance = math.sqrt(

                (driver.latitude - 41.3111) ** 2 +

                (driver.longitude - 69.2797) ** 2

            )

            if distance < min_distance:

                min_distance = distance

                nearest_driver = driver

        order = Order.objects.create(

            customer_name=data['customer'],

            from_location=data['from'],

            to_location=data['to'],

            passengers=data.get(
                'passengers',
                1
            ),

            taxi_type=data.get(
                'taxi_type',
                'economy'
            ),

            status='pending'

        )

        # 🚖 Auto Driver

        if nearest_driver:

            order.driver = nearest_driver

            order.status = 'accepted'

            order.save()

            nearest_driver.status = 'busy'

            nearest_driver.save()

        return JsonResponse({

            'success': True,

            'order_id': order.id

        })

    return JsonResponse({

        'success': False

    })


# =========================
# ACCEPT ORDER
# =========================

@csrf_exempt
def accept_order(request, order_id):

    order = Order.objects.get(
        id=order_id
    )

    driver = Driver.objects.filter(

        status='online',
        online=True

    ).first()

    if driver:

        order.driver = driver

        order.status = 'accepted'

        order.save()

        driver.status = 'busy'

        driver.save()

        return JsonResponse({

            'success': True,

            'driver': driver.name

        })

    return JsonResponse({

        'success': False

    })


# =========================
# DRIVER STATUS
# =========================

@csrf_exempt
def toggle_driver_status(request):

    driver = Driver.objects.first()

    if driver.online:

        driver.online = False

        driver.status = 'offline'

    else:

        driver.online = True

        driver.status = 'online'

    driver.save()

    return JsonResponse({

        'success': True,

        'online': driver.online

    })


# =========================
# DRIVER PANEL
# =========================

def driver_panel(request):

    return render(
        request,
        'driver.html'
    )


# =========================
# REGISTER
# =========================

def register_view(request):

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/')

    return render(

        request,

        'register.html',

        {

            'form': form

        }

    )