from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('map/', views.route_map, name='route_map'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    
    # Journey and booking
    path('journey/<int:journey_id>/', views.journey_detail, name='journey_detail'),
    path('journey/<int:journey_id>/book/', views.book_journey, name='book_journey'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('confirmation/', views.confirmation_redirect, name='confirmation_redirect'),
    
    # API endpoints
    path('api/routes/', views.api_routes, name='api_routes'),
    path('api/journeys-map/', views.api_journeys_map, name='api_journeys_map'),
    path('api/schedule-search/', views.api_schedule_search, name='api_schedule_search'),
]
