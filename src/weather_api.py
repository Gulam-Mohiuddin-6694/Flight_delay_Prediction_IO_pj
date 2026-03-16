import requests
import os

try:
    import config
    CONFIG_API_KEY = getattr(config, 'OPENWEATHER_API_KEY', None)
except ImportError:
    CONFIG_API_KEY = None

class WeatherAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY') or CONFIG_API_KEY
        if not self.api_key:
            raise ValueError("OpenWeather API key not found. Set OPENWEATHER_API_KEY environment variable or in config.py")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """Fetch weather data for a city"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Weather API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching weather: {str(e)}")
            return None
    
    def extract_weather_features(self, weather_data):
        """Extract relevant weather features for ML model"""
        if not weather_data:
            # Return default values if API fails
            return {
                'temperature': 20.0,
                'humidity': 50.0,
                'wind_speed': 5.0,
                'visibility': 10000,
                'pressure': 1013,
                'weather_severity': 0
            }
        
        try:
            features = {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed'],
                'visibility': weather_data.get('visibility', 10000),
                'pressure': weather_data['main']['pressure'],
                'weather_severity': self.calculate_severity(weather_data)
            }
            return features
        except KeyError as e:
            print(f"Error extracting weather features: {str(e)}")
            return self.extract_weather_features(None)
    
    def calculate_severity(self, weather_data):
        """Calculate weather severity index (0-10)"""
        severity = 0
        
        # Check weather conditions
        weather_main = weather_data['weather'][0]['main'].lower()
        if weather_main in ['thunderstorm', 'snow', 'tornado']:
            severity += 5
        elif weather_main in ['rain', 'drizzle']:
            severity += 3
        elif weather_main in ['fog', 'mist', 'haze']:
            severity += 2
        
        # Check wind speed
        wind_speed = weather_data['wind']['speed']
        if wind_speed > 15:
            severity += 3
        elif wind_speed > 10:
            severity += 2
        elif wind_speed > 7:
            severity += 1
        
        # Check visibility
        visibility = weather_data.get('visibility', 10000)
        if visibility < 1000:
            severity += 2
        elif visibility < 5000:
            severity += 1
        
        return min(severity, 10)

# Airport to city mapping with coordinates
AIRPORT_DATA = {
    # US Airports
    'ATL': {'city': 'Atlanta', 'lat': 33.6407, 'lon': -84.4277},
    'ORD': {'city': 'Chicago', 'lat': 41.9742, 'lon': -87.9073},
    'DFW': {'city': 'Dallas', 'lat': 32.8998, 'lon': -97.0403},
    'DEN': {'city': 'Denver', 'lat': 39.8561, 'lon': -104.6737},
    'LAX': {'city': 'Los Angeles', 'lat': 33.9416, 'lon': -118.4085},
    'JFK': {'city': 'New York', 'lat': 40.6413, 'lon': -73.7781},
    'SFO': {'city': 'San Francisco', 'lat': 37.6213, 'lon': -122.3790},
    'LAS': {'city': 'Las Vegas', 'lat': 36.0840, 'lon': -115.1537},
    'SEA': {'city': 'Seattle', 'lat': 47.4502, 'lon': -122.3088},
    'MCO': {'city': 'Orlando', 'lat': 28.4312, 'lon': -81.3081},
    'EWR': {'city': 'Newark', 'lat': 40.6895, 'lon': -74.1745},
    'CLT': {'city': 'Charlotte', 'lat': 35.2144, 'lon': -80.9473},
    'PHX': {'city': 'Phoenix', 'lat': 33.4352, 'lon': -112.0101},
    'IAH': {'city': 'Houston', 'lat': 29.9902, 'lon': -95.3368},
    'MIA': {'city': 'Miami', 'lat': 25.7959, 'lon': -80.2870},
    'BOS': {'city': 'Boston', 'lat': 42.3656, 'lon': -71.0096},
    
    # Indian Airports
    'DEL': {'city': 'Delhi', 'lat': 28.5562, 'lon': 77.1000},
    'BOM': {'city': 'Mumbai', 'lat': 19.0896, 'lon': 72.8656},
    'BLR': {'city': 'Bangalore', 'lat': 13.1986, 'lon': 77.7066},
    'MAA': {'city': 'Chennai', 'lat': 12.9941, 'lon': 80.1709},
    'HYD': {'city': 'Hyderabad', 'lat': 17.2403, 'lon': 78.4294},
    'CCU': {'city': 'Kolkata', 'lat': 22.6520, 'lon': 88.4463},
    'AMD': {'city': 'Ahmedabad', 'lat': 23.0772, 'lon': 72.6347},
    'PNQ': {'city': 'Pune', 'lat': 18.5793, 'lon': 73.9197},
    'GOI': {'city': 'Goa', 'lat': 15.3808, 'lon': 73.8314},
    'COK': {'city': 'Kochi', 'lat': 10.1520, 'lon': 76.4019},
    
    # International Airports
    'DXB': {'city': 'Dubai', 'lat': 25.2532, 'lon': 55.3657},
    'SIN': {'city': 'Singapore', 'lat': 1.3644, 'lon': 103.9915},
    'LHR': {'city': 'London', 'lat': 51.4700, 'lon': -0.4543},
    'CDG': {'city': 'Paris', 'lat': 49.0097, 'lon': 2.5479},
    'FRA': {'city': 'Frankfurt', 'lat': 50.0379, 'lon': 8.5622},
    'HKG': {'city': 'Hong Kong', 'lat': 22.3080, 'lon': 113.9185},
    'NRT': {'city': 'Tokyo', 'lat': 35.7720, 'lon': 140.3929},
    'ICN': {'city': 'Seoul', 'lat': 37.4602, 'lon': 126.4407},
    'BKK': {'city': 'Bangkok', 'lat': 13.6900, 'lon': 100.7501},
    'KUL': {'city': 'Kuala Lumpur', 'lat': 2.7456, 'lon': 101.7072},
    'SYD': {'city': 'Sydney', 'lat': -33.9399, 'lon': 151.1753},
    'MEL': {'city': 'Melbourne', 'lat': -37.6690, 'lon': 144.8410},
}

def calculate_distance(origin, destination):
    """Calculate distance between two airports using Haversine formula"""
    from math import radians, sin, cos, sqrt, atan2
    
    if origin not in AIRPORT_DATA or destination not in AIRPORT_DATA:
        return 1000  # Default distance
    
    lat1, lon1 = AIRPORT_DATA[origin]['lat'], AIRPORT_DATA[origin]['lon']
    lat2, lon2 = AIRPORT_DATA[destination]['lat'], AIRPORT_DATA[destination]['lon']
    
    # Haversine formula
    R = 3959  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return round(distance, 2)

def get_city_from_airport(airport_code):
    """Convert airport code to city name"""
    return AIRPORT_DATA.get(airport_code.upper(), {}).get('city', airport_code)
