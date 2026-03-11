# 🚌 AI Bus Booking System

A modern, full-featured online bus booking platform with interactive route maps, real-time schedules, and AI-powered recommendations.

## ✨ Features

### 🗺️ Interactive Map
- **Live Route Visualization**: Display all bus routes on an interactive map using Leaflet.js
- **Real-Time Bus Tracking**: See current location of buses in transit
- **Route Details**: Click on routes to view distance, fare, and bus information
- **Route Polylines**: Visual representation of entire journey paths

### 📅 Schedule Management
- **Advanced Search**: Filter buses by origin, destination, date, and bus type
- **Detailed Journey Info**: View departure time, arrival time, and estimated duration
- **Seat Availability**: Real-time seat availability tracking
- **Bus Types**: Standard, Express, and Luxury bus classifications
- **Price Display**: Clear pricing per seat and total booking cost

### 🎫 Booking System
- **Seamless Booking Flow**: Easy-to-use booking interface
- **Passenger Information**: Capture name, email, and phone number
- **Multiple Seats**: Book multiple seats in a single transaction
- **Booking Confirmation**: Unique booking reference and confirmation details
- **Order Summary**: Clear breakdown of journey details and costs

### 🔒 Security & Features
- **Secure Transactions**: Safe booking process with unique reference numbers
- **Email Notifications**: Confirmation emails sent to passengers
- **Seat Management**: Prevent double bookings with real-time seat tracking
- **Cancellation Policy**: Clear cancellation and refund information

## 🏗️ Project Structure

```
ai_bus_booking/
├── booking/                          # Django app
│   ├── models.py                    # Database models
│   ├── views.py                     # Business logic
│   ├── forms.py                     # Forms
│   ├── urls.py                      # URL routing
│   ├── admin.py                     # Admin interface
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   └── booking/
│   │       ├── home.html           # Homepage
│   │       ├── map.html            # Interactive map
│   │       ├── schedule.html       # Schedule list
│   │       ├── journey_detail.html # Journey details
│   │       ├── bus_booking/
│   │       │   └── book_route.html # Booking form
│   │       └── confirmation/
│   │           └── confirmation.html # Confirmation page
│   └── migrations/                  # Database migrations
├── static/
│   └── booking/
│       └── style.css               # Global styles
├── busbooking/                      # Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

## 📦 Database Models

### Bus
- bus_number (unique)
- name
- capacity
- bus_type (standard, express, luxury)
- license_plate
- manufacturer
- year
- is_active

### Route
- origin
- destination
- origin_lat, origin_lng (coordinates)
- destination_lat, destination_lng (coordinates)
- distance_km
- duration
- base_fare
- buses (M2M with Bus)
- is_active

### BusJourney
- bus (FK to Bus)
- route (FK to Route)
- departure_time
- arrival_time
- available_seats
- price_per_seat
- status (scheduled, in_transit, completed, cancelled)
- current_lat, current_lng (live tracking)

### Booking
- journey (FK to BusJourney)
- passenger_name
- passenger_email
- passenger_phone
- seats
- total_price
- status (pending, confirmed, completed, cancelled)
- booking_reference (unique)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
git clone <repository-url>
cd ai_bus_booking
```

### Step 2: Create and Activate Virtual Environment
```powershell
# On Windows
python -m venv bus
.\bus\Scripts\activate

# On macOS/Linux
python3 -m venv bus
source bus/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

## 📊 Sample Data Population

### Method 1: Django Admin Interface (GUI)
1. Go to http://127.0.0.1:8000/admin
2. Login with your superuser credentials
3. Add buses, routes, and journeys through the admin interface

### Method 2: Python Shell (Command Line)
```bash
python manage.py shell
```

Then run the following Python commands:

```python
from booking.models import Bus, Route, BusJourney
from datetime import datetime, timedelta

# Create buses
bus1 = Bus.objects.create(
    bus_number="BUS-001",
    name="Express-A",
    capacity=50,
    bus_type="express",
    license_plate="MH-01-AB-1234",
    manufacturer="Volvo",
    year=2023
)

bus2 = Bus.objects.create(
    bus_number="BUS-002",
    name="Luxury-B",
    capacity=40,
    bus_type="luxury",
    license_plate="MH-01-AB-5678",
    manufacturer="Scania",
    year=2023
)

# Create route
route1 = Route.objects.create(
    origin="Mumbai",
    destination="Pune",
    origin_lat=19.0760,
    origin_lng=72.8777,
    destination_lat=18.5204,
    destination_lng=73.8567,
    distance_km=150,
    duration=timedelta(hours=3),
    base_fare=500
)
route1.buses.add(bus1, bus2)

# Create journey
journey1 = BusJourney.objects.create(
    bus=bus1,
    route=route1,
    departure_time=datetime.now() + timedelta(days=1, hours=8),
    arrival_time=datetime.now() + timedelta(days=1, hours=11),
    available_seats=50,
    price_per_seat=600,
    current_lat=19.0760,
    current_lng=72.8777,
    status="scheduled"
)

exit()
```

## 🌐 Available Routes

| URL | Description |
|-----|-------------|
| `/` | Homepage with featured journeys |
| `/map/` | Interactive map with all routes and buses |
| `/schedule/` | Bus schedule search and list |
| `/journey/<id>/` | Journey details page |
| `/journey/<id>/book/` | Booking page for a journey |
| `/confirmation/<id>/` | Booking confirmation |
| `/admin/` | Django admin interface |
| `/api/routes/` | JSON API for all routes |
| `/api/journeys-map/` | JSON API for active journeys |
| `/api/schedule-search/` | JSON API for schedule search |

## 🎨 UI Features

### Homepage
- Hero section with search functionality
- Statistics dashboard
- Featured journeys carousel
- Service features showcase
- Call-to-action buttons

### Map Page
- **Leaflet.js Map**: Interactive map centered on India
- **Route Visualization**: All routes displayed with polylines
- **Journey Markers**: Color-coded markers for journey status
- **Popups**: Click markers to view journey details
- **Live Updates**: Auto-refresh every 30 seconds
- **Legend**: Visual guide to marker meanings

### Schedule Page
- **Advanced Filters**: Search by origin, destination, date, bus type
- **Results Table**: Sortable table with all journey details
- **Pagination**: 10 journeys per page
- **Seat Status**: Color-coded seat availability
- **Quick Booking**: One-click access to booking page

### Booking Page
- **Journey Summary**: Clear display of selected journey
- **Passenger Form**: Name, email, phone, seats input
- **Price Calculator**: Real-time price calculation
- **Booking Terms**: Important information and policies
- **Confirmation**: Unique booking reference

## 🔧 Customization

### Change Primary Colors
Edit `/static/booking/style.css` and update:
```css
--primary: #667eea;
--secondary: #764ba2;
```

### Add New Bus Types
Edit `bus_type` choices in `models.py`:
```python
BUS_TYPE_CHOICES = [
    ('standard', 'Standard Bus'),
    ('express', 'Express Bus'),
    ('luxury', 'Luxury Bus'),
    ('sleeper', 'Sleeper Bus'),  # Add new type
]
```

### Modify Map Coordinates
Update default map center in `templates/booking/map.html`:
```javascript
const map = L.map('map').setView([20.5937, 78.9629], 5);
```

## 📱 API Endpoints

### Get All Routes
```
GET /api/routes/
Response: JSON array of route objects
```

### Get Active Journeys
```
GET /api/journeys-map/
Response: JSON array of journey objects with real-time locations
```

### Search Schedules
```
GET /api/schedule-search/?origin=Mumbai&destination=Pune&date=2024-03-20
Response: JSON array of matching journeys
```

## 🛠️ Technologies Used

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite
- **Maps**: Leaflet.js (Open Street Map)
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6

## 📝 Data Flow

```
User → Homepage
   ↓
Search Journeys (by origin/destination/date)
   ↓
View Results in Schedule or Map
   ↓
Select Journey & Click Book
   ↓
Enter Passenger Details
   ↓
Submit Booking
   ↓
View Confirmation with Booking Reference
   ↓
Receive Email Confirmation
```

## 🚨 Important Notes

1. **Coordinate System**: Routes use latitude/longitude format
2. **Time Zone**: Set in settings.py (default: UTC)
3. **Email**: Configure email backend in settings.py for notifications
4. **Admin Access**: Only superuser can add/edit buses and routes
5. **Database**: SQLite file location: `db.sqlite3`

## 📞 Support

For issues or questions:
1. Check the Django debug page for error details
2. Review Django admin interface for data consistency
3. Check browser console for JavaScript errors
4. Review server logs for backend errors

## 🔐 Security Notes

- Validates seat availability before booking
- Prevents double booking with database transactions
- CSRF protection on all forms
- Input validation on all forms
- SQL injection protection via Django ORM

## 🎓 Learning Resources

- Django Documentation: https://docs.djangoproject.com/
- Leaflet.js Guide: https://leafletjs.com/examples.html
- Bootstrap 5: https://getbootstrap.com/docs/5.0/

## 📄 License

This project is open-source and available for educational purposes.
