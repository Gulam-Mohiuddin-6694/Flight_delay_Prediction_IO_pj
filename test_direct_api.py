import requests

print("Direct API Test")
print("=" * 70)

api_key = "aa073efde7b8d8bbfc867603c35d1566"
url = "https://api.aviationstack.com/v1/flights"

# Test 1: Check API status
print("\n1. Testing API Connection...")
params = {'access_key': api_key, 'limit': 1}

try:
    response = requests.get(url, params=params, timeout=15)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Working: YES")
        print(f"Flights in response: {len(data.get('data', []))}")
        
        if data.get('data'):
            flight = data['data'][0]
            print(f"\nSample Flight:")
            print(f"  Flight: {flight['flight']['iata']}")
            print(f"  Airline: {flight['airline']['name']}")
            print(f"  Route: {flight['departure']['iata']} -> {flight['arrival']['iata']}")
    else:
        print(f"API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Connection Error: {e}")

print("\n" + "=" * 70)
print("If you see 'API Working: YES' above, the API is connected!")
print("=" * 70)
