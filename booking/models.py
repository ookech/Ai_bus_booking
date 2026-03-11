from django.db import models
from datetime import timedelta


class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('standard', 'Standard Bus'),
        ('express', 'Express Bus'),
        ('luxury', 'Luxury Bus'),
    ]
    
    bus_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES, default='standard')
    license_plate = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['bus_number']

    def __str__(self):
        return f"{self.bus_number} - {self.name}"


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    origin_lat = models.FloatField(default=0.0)
    origin_lng = models.FloatField(default=0.0)
    destination_lat = models.FloatField(default=0.0)
    destination_lng = models.FloatField(default=0.0)
    distance_km = models.FloatField(default=0.0)
    duration = models.DurationField(default=timedelta(hours=1))
    base_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    buses = models.ManyToManyField(Bus, related_name='routes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['origin', 'destination']

    def __str__(self):
        return f"{self.origin} to {self.destination}"


class BusJourney(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='journeys')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='journeys')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    current_lat = models.FloatField(default=0.0)
    current_lng = models.FloatField(default=0.0)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-departure_time']

    def __str__(self):
        return f"{self.bus.bus_number} - {self.route} on {self.departure_time}"

    @property
    def estimated_arrival(self):
        return self.arrival_time

    @property
    def booked_seats(self):
        return self.booking_set.aggregate(models.Sum('seats'))['seats__sum'] or 0

    @property
    def remaining_seats(self):
        return self.available_seats - self.booked_seats


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    journey = models.ForeignKey(BusJourney, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=200)
    passenger_email = models.EmailField(blank=True)
    passenger_phone = models.CharField(max_length=20, blank=True)
    seats = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_reference = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.passenger_name} - {self.journey} - Ref: {self.booking_reference}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import uuid
            self.booking_reference = str(uuid.uuid4())[:12].upper()
        if not self.total_price:
            self.total_price = self.seats * self.journey.price_per_seat
        super().save(*args, **kwargs)
