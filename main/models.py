from django.db import models


class Driver(models.Model):

    STATUS_CHOICES = (

        ('online', 'Online'),
        ('offline', 'Offline'),
        ('busy', 'Busy'),

    )

    name = models.CharField(max_length=100)

    car_number = models.CharField(max_length=20)

    phone = models.CharField(
        max_length=20,
        default='+998901234567'
    )

    car_model = models.CharField(
        max_length=100,
        default='Chevrolet Cobalt'
    )

    rating = models.FloatField(default=5.0)

    photo = models.URLField(
        default='https://cdn-icons-png.flaticon.com/512/4140/4140048.png'
    )

    latitude = models.FloatField(default=41.3111)

    longitude = models.FloatField(default=69.2797)

    online = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='online'
    )

    def __str__(self):

        return self.name


class Order(models.Model):

    TAXI_TYPES = (

        ('economy', 'Economy'),
        ('comfort', 'Comfort'),
        ('business', 'Business'),

    )

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('accepted', 'Accepted'),

        ('arrived', 'Arrived'),

        ('started', 'Started'),

        ('completed', 'Completed'),

        ('cancelled', 'Cancelled'),

    )

    customer_name = models.CharField(max_length=100)

    from_location = models.CharField(max_length=200)

    to_location = models.CharField(max_length=200)

    passengers = models.IntegerField(default=1)

    taxi_type = models.CharField(
        max_length=20,
        choices=TAXI_TYPES,
        default='economy'
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    rating = models.IntegerField(default=5)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.customer_name