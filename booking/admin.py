from django.contrib import admin
from .models import Bus, Route, BusJourney, Booking


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'name', 'capacity', 'bus_type', 'is_active')
    list_filter = ('bus_type', 'is_active', 'created_at')
    search_fields = ('bus_number', 'name', 'license_plate')
    fieldsets = (
        ('Basic Information', {
            'fields': ('bus_number', 'name', 'capacity', 'bus_type')
        }),
        ('Vehicle Details', {
            'fields': ('license_plate', 'manufacturer', 'year')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance_km', 'base_fare', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('origin', 'destination')
    filter_horizontal = ('buses',)
    fieldsets = (
        ('Route Information', {
            'fields': ('origin', 'destination', 'distance_km', 'duration', 'base_fare')
        }),
        ('Coordinates', {
            'fields': (
                ('origin_lat', 'origin_lng'),
                ('destination_lat', 'destination_lng')
            )
        }),
        ('Buses', {
            'fields': ('buses',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(BusJourney)
class BusJourneyAdmin(admin.ModelAdmin):
    list_display = ('bus', 'route', 'departure_time', 'arrival_time', 'available_seats', 'price_per_seat', 'status')
    list_filter = ('status', 'departure_time', 'bus__bus_type')
    search_fields = ('bus__bus_number', 'route__origin', 'route__destination')
    date_hierarchy = 'departure_time'
    readonly_fields = ('created_at', 'remaining_seats', 'booked_seats')
    fieldsets = (
        ('Journey Information', {
            'fields': ('bus', 'route', 'status')
        }),
        ('Schedule', {
            'fields': ('departure_time', 'arrival_time')
        }),
        ('Seats & Pricing', {
            'fields': ('available_seats', 'price_per_seat', 'booked_seats', 'remaining_seats')
        }),
        ('Current Location', {
            'fields': (
                ('current_lat', 'current_lng')
            )
        }),
    )
    
    def booked_seats(self, obj):
        return obj.booked_seats
    booked_seats.short_description = 'Booked Seats'
    
    def remaining_seats(self, obj):
        return obj.remaining_seats
    remaining_seats.short_description = 'Remaining Seats'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'passenger_name', 'journey', 'seats', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'journey__route')
    search_fields = ('booking_reference', 'passenger_name', 'passenger_email', 'passenger_phone')
    date_hierarchy = 'created_at'
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference',)
        }),
        ('Passenger Information', {
            'fields': ('passenger_name', 'passenger_email', 'passenger_phone')
        }),
        ('Journey Details', {
            'fields': ('journey', 'seats', 'total_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Log changes
        if change:
            print(f"Booking {obj.booking_reference} updated")
