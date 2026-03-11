"""
Populate sample data for AI Bus Booking System
Run with: python manage.py shell < populate_data.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busbooking.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from booking.models import Bus, Route, BusJourney
from datetime import datetime, timedelta

print("🚀 Starting data population...\n")

# Clear existing data (optional)
# Bus.objects.all().delete()
# Route.objects.all().delete()
# BusJourney.objects.all().delete()

# Create buses
print("📍 Creating buses...")

buses_data = [
    {
        'bus_number': 'BUS-001',
        'name': 'Mumbai Express',
        'capacity': 50,
        'bus_type': 'express',
        'license_plate': 'MH-01-AB-0001',
        'manufacturer': 'Volvo',
        'year': 2023
    },
    {
        'bus_number': 'BUS-002',
        'name': 'Luxury Traveler',
        'capacity': 40,
        'bus_type': 'luxury',
        'license_plate': 'MH-01-AB-0002',
        'manufacturer': 'Scania',
        'year': 2023
    },
    {
        'bus_number': 'BUS-003',
        'name': 'Standard Coach',
        'capacity': 60,
        'bus_type': 'standard',
        'license_plate': 'MH-01-AB-0003',
        'manufacturer': 'Ashok Leyland',
        'year': 2022
    },
    {
        'bus_number': 'BUS-004',
        'name': 'Pune Rapid',
        'capacity': 55,
        'bus_type': 'express',
        'license_plate': 'MH-02-AB-0004',
        'manufacturer': 'Volvo',
        'year': 2023
    },
    {
        'bus_number': 'BUS-005',
        'name': 'Bangalore Express',
        'capacity': 48,
        'bus_type': 'express',
        'license_plate': 'KA-01-AB-0005',
        'manufacturer': 'Scania',
        'year': 2023
    },
]

buses = {}
for bus_data in buses_data:
    bus, created = Bus.objects.get_or_create(
        bus_number=bus_data['bus_number'],
        defaults=bus_data
    )
    buses[bus_data['bus_number']] = bus
    status = "✓ Created" if created else "- Already exists"
    print(f"  {status}: {bus.name} ({bus.bus_number})")

print()

# Create routes
print("🗺️  Creating routes...")

routes_data = [
    {
        'origin': 'Mumbai',
        'destination': 'Pune',
        'origin_lat': 19.0760,
        'origin_lng': 72.8777,
        'destination_lat': 18.5204,
        'destination_lng': 73.8567,
        'distance_km': 150,
        'duration': timedelta(hours=3),
        'base_fare': 500,
        'buses': ['BUS-001', 'BUS-003']
    },
    {
        'origin': 'Mumbai',
        'destination': 'Bangalore',
        'origin_lat': 19.0760,
        'origin_lng': 72.8777,
        'destination_lat': 12.9716,
        'destination_lng': 77.5946,
        'distance_km': 850,
        'duration': timedelta(hours=14),
        'base_fare': 1200,
        'buses': ['BUS-002', 'BUS-005']
    },
    {
        'origin': 'Pune',
        'destination': 'Bangalore',
        'origin_lat': 18.5204,
        'origin_lng': 73.8567,
        'destination_lat': 12.9716,
        'destination_lng': 77.5946,
        'distance_km': 700,
        'duration': timedelta(hours=11),
        'base_fare': 900,
        'buses': ['BUS-004', 'BUS-003']
    },
    {
        'origin': 'Mumbai',
        'destination': 'Ahmedabad',
        'origin_lat': 19.0760,
        'origin_lng': 72.8777,
        'destination_lat': 23.0225,
        'destination_lng': 72.5714,
        'distance_km': 500,
        'duration': timedelta(hours=8),
        'base_fare': 700,
        'buses': ['BUS-001', 'BUS-004']
    },
    {
        'origin': 'Pune',
        'destination': 'Hyderabad',
        'origin_lat': 18.5204,
        'origin_lng': 73.8567,
        'destination_lat': 17.3850,
        'destination_lng': 78.4867,
        'distance_km': 580,
        'duration': timedelta(hours=10),
        'base_fare': 800,
        'buses': ['BUS-002', 'BUS-004']
    },
]

routes = {}
for route_data in routes_data:
    bus_list = route_data.pop('buses')
    route, created = Route.objects.get_or_create(
        origin=route_data['origin'],
        destination=route_data['destination'],
        defaults=route_data
    )
    
    # Add buses to route
    for bus_number in bus_list:
        route.buses.add(buses[bus_number])
    
    route_key = f"{route.origin}-{route.destination}"
    routes[route_key] = route
    status = "✓ Created" if created else "- Already exists"
    print(f"  {status}: {route.origin} → {route.destination} ({route.distance_km}km)")

print()

# Create journeys
print("📅 Creating journeys...")

now = datetime.now()
base_date = now + timedelta(days=1)

journeys_data = [
    # Mumbai to Pune
    {'route': 'Mumbai-Pune', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 8, 'seats': 50, 'price': 600},
    {'route': 'Mumbai-Pune', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 14, 'seats': 35, 'price': 650},
    {'route': 'Mumbai-Pune', 'bus': 'BUS-003', 'date_offset': 0, 'departure_hour': 18, 'seats': 60, 'price': 550},
    
    # Mumbai to Bangalore
    {'route': 'Mumbai-Bangalore', 'bus': 'BUS-002', 'date_offset': 0, 'departure_hour': 20, 'seats': 40, 'price': 1500},
    {'route': 'Mumbai-Bangalore', 'bus': 'BUS-005', 'date_offset': 1, 'departure_hour': 8, 'seats': 48, 'price': 1400},
    
    # Pune to Bangalore
    {'route': 'Pune-Bangalore', 'bus': 'BUS-004', 'date_offset': 0, 'departure_hour': 10, 'seats': 55, 'price': 1100},
    {'route': 'Pune-Bangalore', 'bus': 'BUS-003', 'date_offset': 1, 'departure_hour': 16, 'seats': 50, 'price': 1050},
    
    # Mumbai to Ahmedabad
    {'route': 'Mumbai-Ahmedabad', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 6, 'seats': 45, 'price': 800},
    {'route': 'Mumbai-Ahmedabad', 'bus': 'BUS-004', 'date_offset': 1, 'departure_hour': 12, 'seats': 55, 'price': 750},
    
    # Pune to Hyderabad
    {'route': 'Pune-Hyderabad', 'bus': 'BUS-002', 'date_offset': 0, 'departure_hour': 22, 'seats': 40, 'price': 1000},
    {'route': 'Pune-Hyderabad', 'bus': 'BUS-004', 'date_offset': 1, 'departure_hour': 8, 'seats': 50, 'price': 950},
]

journey_count = 0
for journey_data in journeys_data:
    route_key = journey_data['route']
    route = routes[route_key]
    bus_number = journey_data['bus']
    bus = buses[bus_number]
    
    departure_date = base_date + timedelta(days=journey_data['date_offset'])
    departure_time = departure_date.replace(hour=journey_data['departure_hour'], minute=0, second=0, microsecond=0)
    
    # Calculate arrival time
    journey_duration = route.duration
    arrival_time = departure_time + journey_duration
    
    journey, created = BusJourney.objects.get_or_create(
        bus=bus,
        route=route,
        departure_time=departure_time,
        defaults={
            'arrival_time': arrival_time,
            'available_seats': journey_data['seats'],
            'price_per_seat': journey_data['price'],
            'current_lat': route.origin_lat,
            'current_lng': route.origin_lng,
            'status': 'scheduled'
        }
    )
    
    if created:
        journey_count += 1
        print(f"  ✓ Created: {bus.bus_number} {route.origin}→{route.destination} at {departure_time.strftime('%H:%M')}")

print()
print(f"✅ Data population complete!")
print(f"   • Buses created: {len(buses)}")
print(f"   • Routes created: {len(routes)}")
print(f"   • Journeys created: {journey_count}")
print(f"\n🌐 Access the application at: http://127.0.0.1:8000")
print(f"📊 Admin interface at: http://127.0.0.1:8000/admin")
