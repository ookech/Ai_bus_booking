"""
Django management command to populate sample data for AI Bus Booking System
Usage: python manage.py populate_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.models import Bus, Route, BusJourney
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate sample data for AI Bus Booking System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Clearing existing data...'))
            Bus.objects.all().delete()
            Route.objects.all().delete()
            BusJourney.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        self.stdout.write(self.style.SUCCESS('\n🚀 Starting data population...\n'))

        # Create buses
        self.stdout.write('📍 Creating buses...')
        
        buses_data = [
            {
                'bus_number': 'BUS-001',
                'name': 'Nairobi Express',
                'capacity': 50,
                'bus_type': 'express',
                'license_plate': 'KE-01-AA-0001',
                'manufacturer': 'Volvo',
                'year': 2023
            },
            {
                'bus_number': 'BUS-002',
                'name': 'Luxury Safari',
                'capacity': 40,
                'bus_type': 'luxury',
                'license_plate': 'KE-01-AA-0002',
                'manufacturer': 'Scania',
                'year': 2023
            },
            {
                'bus_number': 'BUS-003',
                'name': 'Standard Coach',
                'capacity': 60,
                'bus_type': 'standard',
                'license_plate': 'KE-01-AA-0003',
                'manufacturer': 'Ashok Leyland',
                'year': 2022
            },
            {
                'bus_number': 'BUS-004',
                'name': 'Coastal Runner',
                'capacity': 55,
                'bus_type': 'express',
                'license_plate': 'KE-02-AA-0004',
                'manufacturer': 'Volvo',
                'year': 2023
            },
            {
                'bus_number': 'BUS-005',
                'name': 'Mombasa Express',
                'capacity': 48,
                'bus_type': 'express',
                'license_plate': 'KE-03-AA-0005',
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
            self.stdout.write(f"  {status}: {bus.name} ({bus.bus_number})")

        self.stdout.write('')

        # Create routes
        self.stdout.write('🗺️  Creating routes...')

        routes_data = [
            {
                'origin': 'Nairobi',
                'destination': 'Mombasa',
                'origin_lat': -1.2921,
                'origin_lng': 36.8219,
                'destination_lat': -4.0435,
                'destination_lng': 39.6682,
                'distance_km': 485,
                'duration': timedelta(hours=7),
                'base_fare': 2500,
                'buses': ['BUS-001', 'BUS-004']
            },
            {
                'origin': 'Nairobi',
                'destination': 'Nakuru',
                'origin_lat': -1.2921,
                'origin_lng': 36.8219,
                'destination_lat': -0.3031,
                'destination_lng': 35.8696,
                'distance_km': 160,
                'duration': timedelta(hours=2, minutes=30),
                'base_fare': 1000,
                'buses': ['BUS-001', 'BUS-003']
            },
            {
                'origin': 'Nairobi',
                'destination': 'Kisumu',
                'origin_lat': -1.2921,
                'origin_lng': 36.8219,
                'destination_lat': -0.1022,
                'destination_lng': 34.7617,
                'distance_km': 355,
                'duration': timedelta(hours=5),
                'base_fare': 1800,
                'buses': ['BUS-002', 'BUS-005']
            },
            {
                'origin': 'Mombasa',
                'destination': 'Nakuru',
                'origin_lat': -4.0435,
                'origin_lng': 39.6682,
                'destination_lat': -0.3031,
                'destination_lng': 35.8696,
                'distance_km': 520,
                'duration': timedelta(hours=8),
                'base_fare': 2200,
                'buses': ['BUS-004', 'BUS-005']
            },
            {
                'origin': 'Nakuru',
                'destination': 'Kericho',
                'origin_lat': -0.3031,
                'origin_lng': 35.8696,
                'destination_lat': -0.3667,
                'destination_lng': 35.2833,
                'distance_km': 95,
                'duration': timedelta(hours=2),
                'base_fare': 800,
                'buses': ['BUS-001', 'BUS-002']
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
            self.stdout.write(f"  {status}: {route.origin} → {route.destination} ({route.distance_km}km)")

        self.stdout.write('')

        # Create journeys
        self.stdout.write('📅 Creating journeys...')

        now = timezone.now()
        base_date = now + timedelta(days=1)

        journeys_data = [
            # Nairobi to Mombasa
            {'route': 'Nairobi-Mombasa', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 8, 'seats': 50, 'price': 3000},
            {'route': 'Nairobi-Mombasa', 'bus': 'BUS-004', 'date_offset': 0, 'departure_hour': 14, 'seats': 35, 'price': 3200},
            {'route': 'Nairobi-Mombasa', 'bus': 'BUS-005', 'date_offset': 1, 'departure_hour': 20, 'seats': 40, 'price': 2800},
            
            # Nairobi to Nakuru
            {'route': 'Nairobi-Nakuru', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 9, 'seats': 45, 'price': 1200},
            {'route': 'Nairobi-Nakuru', 'bus': 'BUS-003', 'date_offset': 0, 'departure_hour': 16, 'seats': 55, 'price': 1100},
            
            # Nairobi to Kisumu
            {'route': 'Nairobi-Kisumu', 'bus': 'BUS-002', 'date_offset': 0, 'departure_hour': 7, 'seats': 40, 'price': 2200},
            {'route': 'Nairobi-Kisumu', 'bus': 'BUS-005', 'date_offset': 1, 'departure_hour': 11, 'seats': 48, 'price': 2000},
            
            # Mombasa to Nakuru
            {'route': 'Mombasa-Nakuru', 'bus': 'BUS-004', 'date_offset': 0, 'departure_hour': 10, 'seats': 55, 'price': 2700},
            {'route': 'Mombasa-Nakuru', 'bus': 'BUS-005', 'date_offset': 1, 'departure_hour': 15, 'seats': 50, 'price': 2500},
            
            # Nakuru to Kericho
            {'route': 'Nakuru-Kericho', 'bus': 'BUS-001', 'date_offset': 0, 'departure_hour': 12, 'seats': 50, 'price': 900},
            {'route': 'Nakuru-Kericho', 'bus': 'BUS-002', 'date_offset': 1, 'departure_hour': 9, 'seats': 40, 'price': 850},
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
                self.stdout.write(f"  ✓ {bus.bus_number} {route.origin}→{route.destination} at {departure_time.strftime('%H:%M')}")

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Data population complete!'))
        self.stdout.write(f'   • Buses created: {len(buses)}')
        self.stdout.write(f'   • Routes created: {len(routes)}')
        self.stdout.write(f'   • Journeys created: {journey_count}')
        self.stdout.write(self.style.WARNING('\n🌐 Access the application at: http://127.0.0.1:8000'))
        self.stdout.write(self.style.WARNING('📊 Admin interface at: http://127.0.0.1:8000/admin'))
