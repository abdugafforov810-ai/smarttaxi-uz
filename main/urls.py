from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [

    path('', home),

    path('drivers-api/', drivers_api),

    path('orders-api/', orders_api),

    path('create-order/', create_order),

    path('register/', register_view),

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

]