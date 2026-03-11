# 🚀 Quick Start Guide - AI Bus Booking System

## ⚡ 5-Minute Setup

### Step 1: Activate Virtual Environment
```powershell
.\bus\Scripts\activate
```

### Step 2: Install Dependencies (if not already done)
```powershell
pip install -r requirements.txt
```

### Step 3: Create Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin Account
```powershell
python manage.py createsuperuser
# Follow prompts to create username/password
```

### Step 5: Load Sample Data
```powershell
python manage.py populate_data
```

### Step 6: Start Server
```powershell
python manage.py runserver
```

## 🌐 Access Your Site

| Page | URL |
|------|-----|
| **Homepage** | http://127.0.0.1:8000 |
| **Interactive Map** | http://127.0.0.1:8000/map/ |
| **Bus Schedule** | http://127.0.0.1:8000/schedule/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |

---

## 📋 What You Have

### ✅ Fully Implemented Features

1. **Interactive Map** 🗺️
   - Leaflet.js powered map showing all routes
   - Live bus location markers
   - Route details on click
   - Auto-refresh every 30 seconds
   - Color-coded journey status

2. **Schedule System** 📅
   - Search journeys by origin/destination/date
   - Real-time seat availability
   - Departure and arrival times displayed
   - Pagination for results
   - Filter by bus type

3. **Booking Engine** 🎫
   - Complete booking workflow
   - Passenger information capture
   - Automatic price calculation
   - Unique booking reference
   - Confirmation page

4. **Admin Dashboard** 👨‍💼
   - Manage buses, routes, journeys, bookings
   - Advanced filtering and search
   - Organize data with fieldsets
   - Easy data entry forms

---

## 🎯 Main Pages Explained

### **Home Page** (`/`)
- Hero section with search box
- Featured journeys carousel
- Service statistics
- Why choose us section
- Call-to-action buttons

**Features:**
- Search by city and date
- See featured buses with pricing
- Quick links to map and schedules

### **Map Page** (`/map/`)
- Interactive Leaflet.js map
- All routes displayed with lines
- Bus markers showing live locations
- Click markers for journey info
- Live updates every 30 seconds

**What You Can Do:**
- Explore all available routes
- See active journeys
- Check bus locations in real-time
- View journey details via popups

### **Schedule Page** (`/schedule/`)
- Search form at top
- Results table with all details
- Pagination support
- Seat availability status
- Quick book buttons

**How to Search:**
1. Enter "From" city (e.g., "Mumbai")
2. Enter "To" city (e.g., "Pune")
3. Select departure date
4. (Optional) Filter by bus type
5. Click "Search"

### **Booking Page** (`/journey/<id>/book/`)
- Journey details summary
- Passenger form
- Seat selection
- Price calculation
- Booking terms

**Booking Process:**
1. Fill passenger name (required)
2. Add email and phone (optional)
3. Select number of seats
4. Review pricing on right sidebar
5. Click "Proceed to Payment"

### **Confirmation Page** (`/confirmation/<id>/`)
- Booking reference number
- All journey details
- Passenger information
- Important instructions
- Support contact info

---

## 🗺️ Sample Data Included

### Buses (5 total)
- **BUS-001**: Mumbai Express (50 seats, Express)
- **BUS-002**: Luxury Traveler (40 seats, Luxury)
- **BUS-003**: Standard Coach (60 seats, Standard)
- **BUS-004**: Pune Rapid (55 seats, Express)
- **BUS-005**: Bangalore Express (48 seats, Express)

### Routes (5 total)
1. **Mumbai → Pune** (150 km, 3h)
2. **Mumbai → Bangalore** (850 km, 14h)
3. **Pune → Bangalore** (700 km, 11h)
4. **Mumbai → Ahmedabad** (500 km, 8h)
5. **Pune → Hyderabad** (580 km, 10h)

### Journeys (10 total)
- Multiple departures per route
- Starting tomorrow with various times
- Different seat availabilities
- Multiple journeys at peak hours

---

## 🛠️ Customization Guide

### Change Theme Colors
Edit `/static/booking/style.css`:
```css
:root {
    --primary: #667eea;      /* Main color */
    --secondary: #764ba2;    /* Secondary color */
    --success: #30b570;      /* Success color */
}
```

### Add More Sample Data
```powershell
python manage.py populate_data --clear
```
(The `--clear` flag removes old data first)

### Add a New Route
1. Go to Admin Panel → Routes → Add Route
2. Enter origin, destination, coordinates
3. Enter distance and duration
4. Set base fare
5. Assign buses to route
6. Save

### Add a Bus Journey
1. Go to Admin Panel → Bus Journeys → Add
2. Select bus and route
3. Set departure/arrival times
4. Set available seats and price
5. Save

---

## 🔍 Testing the System

### Test a Booking
1. Go to home page (`/`)
2. Search for any route (e.g., Mumbai → Pune)
3. View results on Schedule page
4. Click "View Details" on any journey
5. Click "Book Now"
6. Fill passenger details:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Phone: "9876543210"
   - Seats: "2"
7. Click "Proceed to Payment"
8. View confirmation page

### View on Map
1. Go to Map page (`/map/`)
2. Scroll to see all routes
3. Click on journey cards to see details
4. Watch for real-time updates

### Try Admin Panel
1. Go to Admin (`/admin/`)
2. Login with superuser credentials
3. Explore Buses, Routes, Journeys, Bookings
4. Try filtering and searching
5. Add test data

---

## 📱 Features Checklist

✅ Interactive map with Leaflet.js
✅ Route visualization with polylines
✅ Real-time bus location markers
✅ Advanced schedule search
✅ Seat availability tracking
✅ Multi-step booking process
✅ Booking confirmations
✅ Admin interface
✅ Sample data included
✅ Responsive design
✅ API endpoints for data
✅ Email field support
✅ Unique booking references

---

## 🐛 Troubleshooting

### "No module named 'booking'"
- Make sure you're in the project root directory
- Check that the booking app is in INSTALLED_APPS

### "Database locked" error
- Close other instances of the server
- Delete `db.sqlite3` and run migrations again

### Map doesn't load
- Check browser console for JavaScript errors
- Ensure Leaflet.js URL is accessible
- Check internet connection (needs OpenStreetMap tiles)

### No journeys showing
- Run `python manage.py populate_data`
- Check Admin panel to verify data exists
- Ensure journeys have future departure dates

---

## 📞 Support Commands

```powershell
# Check for errors
python manage.py check

# View all routes in database
python manage.py shell
>>> from booking.models import Route
>>> Route.objects.all()

# Running tests (if written)
python manage.py test

# Reset database completely
python manage.py flush

# See migrations status
python manage.py showmigrations
```

---

## 🎓 Next Steps

1. **Test all features** - Book a ticket through the system
2. **Explore Admin** - Add/edit buses and routes
3. **Check API endpoints** - Visit `/api/routes/`, `/api/journeys-map/`
4. **Customize colors** - Update CSS to match your brand
5. **Add email config** - Set up email for confirmations
6. **Deploy** - Move to production server

---

**Happy Booking! 🚀**

For detailed documentation, see [README.md](README.md)
