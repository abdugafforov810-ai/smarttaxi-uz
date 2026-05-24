from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'drivers-api/',
        views.drivers_api
    ),

    path(
        'orders-api/',
        views.orders_api
    ),

    path(
        'create-order/',
        views.create_order
    ),

    path(
        'accept-order/<int:order_id>/',
        views.accept_order
    ),

    path(
        'toggle-driver-status/',
        views.toggle_driver_status
    ),

]