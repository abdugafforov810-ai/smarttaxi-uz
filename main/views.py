from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Driver, Order

import random
import json
import math


# =========================
# HOME PAGE
# =========================

@login_required
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
            online=True
        )

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

            status='accepted'

        )

        if nearest_driver:

            order.driver = nearest_driver

            order.save()

        return JsonResponse({

            'success': True

        })

    return JsonResponse({

        'success': False

    })


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