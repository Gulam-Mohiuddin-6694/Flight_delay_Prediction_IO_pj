import requests
import json

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city):
        """Fetch weather data for a given city/airport"""
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
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def extract_features(self, weather_data):
        """Extract relevant features from weather API response"""
        if not weather_data:
            return self.get_default_weather()
        
        try:
            features = {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'wind_speed': weather_data['wind']['speed'],
                'visibility': weather_data.get('visibility', 10000) / 1000,  # Convert to km
                'weather_condition': weather_data['weather'][0]['main'],
                'weather_description': weather_data['weather'][0]['description']
            }
            
            # Calculate weather severity score (0-10)
            features['weather_severity'] = self.calculate_severity(features)
            
            return features
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return self.get_default_weather()
    
    def calculate_severity(self, features):
        """Calculate weather severity score based on conditions"""
        severity = 0
        
        # Wind speed impact
        if features['wind_speed'] > 20:
            severity += 4
        elif features['wind_speed'] > 15:
            severity += 3
        elif features['wind_speed'] > 10:
            severity += 2
        elif features['wind_speed'] > 5:
            severity += 1
        
        # Visibility impact
        if features['visibility'] < 2:
            severity += 4
        elif features['visibility'] < 5:
            severity += 2
        elif features['visibility'] < 8:
            severity += 1
        
        # Weather condition impact
        bad_conditions = ['Rain', 'Thunderstorm', 'Snow', 'Fog', 'Mist', 'Drizzle']
        if features['weather_condition'] in bad_conditions:
            severity += 2
        
        return min(severity, 10)
    
    def get_default_weather(self):
        """Return default weather features when API fails"""
        return {
            'temperature': 20.0,
            'humidity': 50.0,
            'pressure': 1013.0,
            'wind_speed': 5.0,
            'visibility': 10.0,
            'weather_condition': 'Clear',
            'weather_description': 'clear sky',
            'weather_severity': 0
        }
    
    def display_weather(self, features):
        """Display weather information"""
        print("\n" + "="*50)
        print("WEATHER CONDITIONS")
        print("="*50)
        print(f"Condition: {features['weather_description'].title()}")
        print(f"Temperature: {features['temperature']:.1f}°C")
        print(f"Humidity: {features['humidity']:.0f}%")
        print(f"Wind Speed: {features['wind_speed']:.1f} m/s")
        print(f"Visibility: {features['visibility']:.1f} km")
        print(f"Pressure: {features['pressure']:.0f} hPa")
        print(f"Weather Severity Score: {features['weather_severity']}/10")
        print("="*50 + "\n")

# Airport to city mapping (for common US airports)
AIRPORT_CITY_MAP = {
    'ATL': 'Atlanta', 'DFW': 'Dallas', 'DEN': 'Denver', 'ORD': 'Chicago',
    'LAX': 'Los Angeles', 'JFK': 'New York', 'LAS': 'Las Vegas', 'MCO': 'Orlando',
    'MIA': 'Miami', 'CLT': 'Charlotte', 'SEA': 'Seattle', 'PHX': 'Phoenix',
    'EWR': 'Newark', 'SFO': 'San Francisco', 'IAH': 'Houston', 'BOS': 'Boston',
    'MSP': 'Minneapolis', 'DTW': 'Detroit', 'PHL': 'Philadelphia', 'LGA': 'New York',
    'FLL': 'Fort Lauderdale', 'BWI': 'Baltimore', 'DCA': 'Washington',
    'MDW': 'Chicago', 'SLC': 'Salt Lake City', 'IAD': 'Washington', 'SAN': 'San Diego'
}

def get_city_from_airport(airport_code):
    """Convert airport code to city name"""
    return AIRPORT_CITY_MAP.get(airport_code.upper(), airport_code)
