from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
import json

from .models import Route, Bus, BusJourney, Booking
from .forms import BookingForm, ScheduleSearchForm, ContactForm


def home(request):
    """Display home page with featured routes and map overview"""
    routes = Route.objects.filter(is_active=True)
    journeys = BusJourney.objects.filter(
        status='scheduled',
        departure_time__gte=datetime.now()
    ).select_related('bus', 'route')[:10]
    
    context = {
        'routes': routes,
        'featured_journeys': journeys,
        'total_buses': Bus.objects.filter(is_active=True).count(),
        'total_routes': routes.count(),
    }
    return render(request, 'booking/home.html', context)


def route_map(request):
    """Display interactive map with all routes and buses"""
    routes = Route.objects.filter(is_active=True).prefetch_related('journeys')
    journeys = BusJourney.objects.filter(
        status__in=['scheduled', 'in_transit'],
        departure_time__gte=datetime.now() - timedelta(hours=24)
    ).select_related('bus', 'route')
    
    context = {
        'routes': routes,
        'journeys': journeys,
        'map_center': [-0.0236, 37.9062],  # Kenya center coordinates
    }
    return render(request, 'booking/map.html', context)


def schedule_list(request):
    """Display bus schedules with search functionality"""
    form = ScheduleSearchForm(request.GET or None)
    journeys = BusJourney.objects.filter(
        status='scheduled',
        departure_time__gte=datetime.now()
    ).select_related('bus', 'route').order_by('departure_time')
    
    if form.is_valid():
        origin = form.cleaned_data.get('origin')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')
        bus_type = form.cleaned_data.get('bus_type')
        
        if origin:
            journeys = journeys.filter(route__origin__icontains=origin)
        if destination:
            journeys = journeys.filter(route__destination__icontains=destination)
        if departure_date:
            next_day = departure_date + timedelta(days=1)
            journeys = journeys.filter(
                departure_time__date=departure_date
            )
        if bus_type:
            journeys = journeys.filter(bus__bus_type=bus_type)
    
    # Pagination
    paginator = Paginator(journeys, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'journeys': page_obj,
    }
    return render(request, 'booking/schedule.html', context)


def journey_detail(request, journey_id):
    """Display detailed information about a specific journey"""
    journey = get_object_or_404(BusJourney, id=journey_id)
    
    context = {
        'journey': journey,
        'remaining_seats': journey.remaining_seats,
        'booked_seats': journey.booked_seats,
    }
    return render(request, 'booking/journey_detail.html', context)


def book_journey(request, journey_id):
    """Handle booking for a specific journey"""
    journey = get_object_or_404(BusJourney, id=journey_id)
    
    if journey.remaining_seats <= 0:
        return render(request, 'booking/bus_booking/book_route.html', {
            'error': 'No seats available for this journey',
            'journey': journey
        })
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.journey = journey
            
            # Check if enough seats available
            if booking.seats > journey.remaining_seats:
                form.add_error('seats', f'Only {journey.remaining_seats} seats available')
                return render(request, 'booking/bus_booking/book_route.html', {
                    'form': form,
                    'journey': journey
                })
            
            booking.save()
            return redirect(reverse('booking:confirmation', args=[booking.id]))
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'journey': journey,
        'remaining_seats': journey.remaining_seats,
    }
    return render(request, 'booking/bus_booking/book_route.html', context)


def confirmation(request, booking_id):
    """Display booking confirmation"""
    booking = get_object_or_404(Booking, id=booking_id)
    context = {'booking': booking}
    return render(request, 'booking/confirmation/confirmation.html', context)


def confirmation_redirect(request):
    """Redirect for confirmation"""
    return render(request, 'booking/confirmation/confirmation_redirect.html', {
        'message': 'Please book a journey first to view confirmation.'
    })


# API ENDPOINTS FOR AJAX/MAP FUNCTIONALITY

@require_http_methods(["GET"])
def api_routes(request):
    """API endpoint returning all routes as JSON for map"""
    routes = Route.objects.filter(is_active=True).values(
        'id', 'origin', 'destination',
        'origin_lat', 'origin_lng',
        'destination_lat', 'destination_lng',
        'distance_km', 'base_fare'
    )
    return JsonResponse(list(routes), safe=False)


@require_http_methods(["GET"])
def api_journeys_map(request):
    """API endpoint returning active journeys for map visualization"""
    journeys = BusJourney.objects.filter(
        status__in=['scheduled', 'in_transit'],
        departure_time__gte=datetime.now() - timedelta(hours=24)
    ).values(
        'id', 'bus__bus_number', 'bus__name', 'bus__bus_type',
        'route__origin', 'route__destination',
        'current_lat', 'current_lng',
        'departure_time', 'arrival_time',
        'available_seats', 'price_per_seat', 'status'
    )
    
    # Calculate remaining seats for each journey
    journey_list = list(journeys)
    for journey in journey_list:
        journey['remaining_seats'] = journey['available_seats'] - (
            Booking.objects.filter(
                journey_id=journey['id'],
                status__in=['pending', 'confirmed']
            ).aggregate(
                total=sum(models.F('seats'), output_field=models.IntegerField())
            )['total'] or 0
        )
    
    return JsonResponse(journey_list, safe=False)


@require_http_methods(["GET"])
def api_schedule_search(request):
    """API endpoint for schedule search"""
    origin = request.GET.get('origin', '').strip()
    destination = request.GET.get('destination', '').strip()
    date_str = request.GET.get('date', '')
    
    journeys = BusJourney.objects.filter(
        status='scheduled',
        departure_time__gte=datetime.now()
    ).select_related('bus', 'route')
    
    if origin:
        journeys = journeys.filter(route__origin__icontains=origin)
    if destination:
        journeys = journeys.filter(route__destination__icontains=destination)
    if date_str:
        try:
            search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            journeys = journeys.filter(departure_time__date=search_date)
        except ValueError:
            pass
    
    data = [{
        'id': j.id,
        'bus_number': j.bus.bus_number,
        'bus_type': j.bus.bus_type,
        'origin': j.route.origin,
        'destination': j.route.destination,
        'departure': j.departure_time.isoformat(),
        'arrival': j.arrival_time.isoformat(),
        'remaining_seats': j.remaining_seats,
        'price_per_seat': float(j.price_per_seat),
    } for j in journeys[:20]]
    
    return JsonResponse(data, safe=False)


def contact(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the contact form
            # In a real application, you would send an email here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Here you could save to a Contact model or send email
            # For now, we'll just display a success message
            context = {
                'form': form,
                'submitted': True,
                'name': name,
            }
            return render(request, 'booking/contact.html', context)
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'submitted': False,
    }
    return render(request, 'booking/contact.html', context)

