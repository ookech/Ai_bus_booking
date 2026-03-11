# 🔌 API Documentation - AI Bus Booking System

## Overview

The AI Bus Booking System provides REST JSON APIs for retrieving bus routes, journeys, and searching schedules. These endpoints can be used to build mobile apps, integrations, or custom client applications.

## Base URL
```
http://127.0.0.1:8000
```

All endpoints return JSON responses.

---

## 📍 Endpoints

### 1. Get All Routes
Retrieve all available bus routes with their details and coordinates.

**Request:**
```
GET /api/routes/
```

**Response:**
```json
[
    {
        "id": 1,
        "origin": "Mumbai",
        "destination": "Pune",
        "origin_lat": 19.0760,
        "origin_lng": 72.8777,
        "destination_lat": 18.5204,
        "destination_lng": 73.8567,
        "distance_km": 150,
        "base_fare": 500
    },
    {
        "id": 2,
        "origin": "Mumbai",
        "destination": "Bangalore",
        "origin_lat": 19.0760,
        "origin_lng": 72.8777,
        "destination_lat": 12.9716,
        "destination_lng": 77.5946,
        "distance_km": 850,
        "base_fare": 1200
    }
]
```

**Usage Example (JavaScript):**
```javascript
fetch('/api/routes/')
    .then(response => response.json())
    .then(routes => {
        routes.forEach(route => {
            console.log(`${route.origin} → ${route.destination}: ${route.distance_km}km`);
        });
    });
```

---

### 2. Get Active Journeys (Map Data)
Retrieve all active/scheduled journeys with real-time location data.

**Request:**
```
GET /api/journeys-map/
```

**Response:**
```json
[
    {
        "id": 1,
        "bus__bus_number": "BUS-001",
        "bus__name": "Mumbai Express",
        "bus__bus_type": "express",
        "route__origin": "Mumbai",
        "route__destination": "Pune",
        "current_lat": 19.0760,
        "current_lng": 72.8777,
        "departure_time": "2024-03-12T08:00:00Z",
        "arrival_time": "2024-03-12T11:00:00Z",
        "available_seats": 50,
        "price_per_seat": 600,
        "status": "scheduled",
        "remaining_seats": 45
    }
]
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | int | Journey ID |
| bus__bus_number | string | Bus registration number |
| bus__name | string | Bus name/identifier |
| bus__bus_type | string | Bus type (standard/express/luxury) |
| route__origin | string | Journey starting point |
| route__destination | string | Journey ending point |
| current_lat | float | Current latitude of bus |
| current_lng | float | Current longitude of bus |
| departure_time | datetime | Journey departure time (ISO 8601) |
| arrival_time | datetime | Journey arrival time (ISO 8601) |
| available_seats | int | Total available seats |
| price_per_seat | decimal | Price per seat in INR |
| status | string | Journey status (scheduled/in_transit/completed/cancelled) |
| remaining_seats | int | Remaining seats (calculated) |

**Usage Example (JavaScript):**
```javascript
fetch('/api/journeys-map/')
    .then(response => response.json())
    .then(journeys => {
        journeys.forEach(journey => {
            const marker = L.circleMarker([journey.current_lat, journey.current_lng])
                .bindPopup(`${journey.bus__bus_number}: ${journey.remaining_seats} seats`)
                .addTo(map);
        });
    });
```

---

### 3. Search Schedules
Search for available buses based on criteria.

**Request:**
```
GET /api/schedule-search/?origin=Mumbai&destination=Pune&date=2024-03-15
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| origin | string | Yes | Departure city |
| destination | string | Yes | Arrival city |
| date | string | No | Departure date (YYYY-MM-DD) |

**Response:**
```json
[
    {
        "id": 1,
        "bus_number": "BUS-001",
        "bus_type": "express",
        "origin": "Mumbai",
        "destination": "Pune",
        "departure": "2024-03-15T08:00:00Z",
        "arrival": "2024-03-15T11:00:00Z",
        "remaining_seats": 45,
        "price_per_seat": 600.00
    },
    {
        "id": 2,
        "bus_number": "BUS-003",
        "bus_type": "standard",
        "origin": "Mumbai",
        "destination": "Pune",
        "departure": "2024-03-15T18:00:00Z",
        "arrival": "2024-03-15T21:00:00Z",
        "remaining_seats": 60,
        "price_per_seat": 550.00
    }
]
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | int | Journey ID |
| bus_number | string | Bus registration number |
| bus_type | string | Bus type classification |
| origin | string | Departure city |
| destination | string | Arrival city |
| departure | datetime | Departure time (ISO 8601) |
| arrival | datetime | Arrival time (ISO 8601) |
| remaining_seats | int | Available seats remaining |
| price_per_seat | decimal | Price per seat in INR |

**Usage Example (JavaScript):**
```javascript
const searchParams = {
    origin: 'Mumbai',
    destination: 'Pune',
    date: '2024-03-15'
};

const queryString = new URLSearchParams(searchParams).toString();
fetch(`/api/schedule-search/?${queryString}`)
    .then(response => response.json())
    .then(journeys => {
        console.log(`Found ${journeys.length} journeys`);
        journeys.forEach(j => {
            console.log(`${j.bus_number}: ${j.departure} (₹${j.price_per_seat})`);
        });
    });
```

---

## 🔍 Example Integrations

### React Component - Journey List
```jsx
import { useState, useEffect } from 'react';

function JourneyList({ origin, destination, date }) {
    const [journeys, setJourneys] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const params = new URLSearchParams({ origin, destination, date }).toString();
        fetch(`/api/schedule-search/?${params}`)
            .then(res => res.json())
            .then(data => {
                setJourneys(data);
                setLoading(false);
            });
    }, [origin, destination, date]);

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            {journeys.map(journey => (
                <div key={journey.id} className="journey-card">
                    <h3>{journey.bus_number}</h3>
                    <p>Departs: {new Date(journey.departure).toLocaleString()}</p>
                    <p>Seats Available: {journey.remaining_seats}</p>
                    <p>Price: ₹{journey.price_per_seat}</p>
                    <button onClick={() => bookJourney(journey.id)}>
                        Book Now
                    </button>
                </div>
            ))}
        </div>
    );
}

export default JourneyList;
```

### Node.js API Client
```javascript
const fetch = require('node-fetch');

class BusBookingAPI {
    constructor(baseURL = 'http://127.0.0.1:8000') {
        this.baseURL = baseURL;
    }

    async getRoutes() {
        const response = await fetch(`${this.baseURL}/api/routes/`);
        return await response.json();
    }

    async getJourneys() {
        const response = await fetch(`${this.baseURL}/api/journeys-map/`);
        return await response.json();
    }

    async searchSchedules(origin, destination, date) {
        const params = new URLSearchParams({ origin, destination, date });
        const response = await fetch(
            `${this.baseURL}/api/schedule-search/?${params}`
        );
        return await response.json();
    }
}

// Usage
const api = new BusBookingAPI();
api.searchSchedules('Mumbai', 'Pune', '2024-03-15')
    .then(journeys => console.log(journeys))
    .catch(error => console.error(error));
```

---

## 🗺️ Map Integration Example

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        #map { height: 600px; }
    </style>
</head>
<body>
    <div id="map"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Create map
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // Load routes
        fetch('/api/routes/')
            .then(r => r.json())
            .then(routes => {
                routes.forEach(route => {
                    // Draw route line
                    L.polyline([
                        [route.origin_lat, route.origin_lng],
                        [route.destination_lat, route.destination_lng]
                    ], { color: 'blue' }).addTo(map);

                    // Add markers
                    L.marker([route.origin_lat, route.origin_lng])
                        .bindPopup(route.origin)
                        .addTo(map);
                    
                    L.marker([route.destination_lat, route.destination_lng])
                        .bindPopup(route.destination)
                        .addTo(map);
                });
            });

        // Load journeys
        fetch('/api/journeys-map/')
            .then(r => r.json())
            .then(journeys => {
                journeys.forEach(j => {
                    L.circleMarker([j.current_lat, j.current_lng], {
                        radius: 8,
                        fillColor: '#FF6B6B',
                        color: '#fff',
                        weight: 2
                    })
                    .bindPopup(`${j.bus__bus_number}: ${j.remaining_seats} seats`)
                    .addTo(map);
                });
            });
    </script>
</body>
</html>
```

---

## 📊 Data Format

### Datetime Format
All timestamps are in ISO 8601 format with UTC timezone:
```
2024-03-12T08:00:00Z
```

Parse in JavaScript:
```javascript
const date = new Date('2024-03-12T08:00:00Z');
console.log(date.toLocaleString()); // Local time
```

### Currency
All prices are in Indian Rupees (INR):
```
"price_per_seat": 600.00
```

### Coordinates (GIS)
Latitude/Longitude format following WGS84:
```
"origin_lat": 19.0760,
"origin_lng": 72.8777
```

---

## ✅ Error Handling

APIs currently return data or empty arrays. For errors, check HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | Not found |
| 500 | Server error |

**Example error handling:**
```javascript
fetch('/api/schedule-search/?origin=Mumbai')
    .then(response => {
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return response.json();
    })
    .catch(error => console.error(error));
```

---

## 🔐 Security

- **No authentication required** for read-only APIs
- **CORS enabled** for browser requests
- **Rate limiting** (if deployed)

For production, consider:
- Adding API key authentication
- Implementing rate limiting
- Using HTTPS
- Adding request validation

---

## 📱 Mobile App Example (React Native)

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity } from 'react-native';

export default function BusSearch() {
    const [journeys, setJourneys] = useState([]);

    useEffect(() => {
        fetch('http://192.168.1.100:8000/api/schedule-search/?origin=Mumbai&destination=Pune')
            .then(r => r.json())
            .then(data => setJourneys(data));
    }, []);

    return (
        <View>
            <FlatList
                data={journeys}
                keyExtractor={item => item.id.toString()}
                renderItem={({ item }) => (
                    <TouchableOpacity style={{ padding: 10, borderBottomWidth: 1 }}>
                        <Text>{item.bus_number}</Text>
                        <Text>{item.departure}</Text>
                        <Text>₹{item.price_per_seat}</Text>
                    </TouchableOpacity>
                )}
            />
        </View>
    );
}
```

---

## 🚀 Deployment Notes

When deploying to production:

1. **Update ALLOWED_HOSTS** in settings.py
2. **Enable HTTPS** for API calls
3. **Add API authentication** if needed
4. **Configure CORS** for cross-origin requests:
   ```python
   # Add to settings.py
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
   ]
   ```
5. **Add API documentation** with Swagger/OpenAPI
6. **Implement rate limiting** with django-ratelimit

---

## 📞 Support

For API issues, check:
1. Django debug toolbar
2. Browser Network tab
3. Server logs
4. Database query count

Run Django checks:
```bash
python manage.py check
```
