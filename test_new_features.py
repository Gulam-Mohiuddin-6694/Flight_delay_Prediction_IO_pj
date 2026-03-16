import sys
sys.path.append('src')

from weather_api import calculate_distance, AIRPORT_DATA
from datetime import datetime

print("=" * 60)
print("Testing New Features")
print("=" * 60)

# Test 1: Distance calculation
print("\n1. Testing Distance Calculation:")
print("-" * 60)

test_routes = [
    ('DEL', 'BOM', 'Delhi to Mumbai'),
    ('BLR', 'DEL', 'Bangalore to Delhi'),
    ('JFK', 'LAX', 'New York to Los Angeles'),
    ('DEL', 'DXB', 'Delhi to Dubai'),
    ('BOM', 'LHR', 'Mumbai to London'),
]

for origin, dest, route_name in test_routes:
    distance = calculate_distance(origin, dest)
    print(f"{route_name}: {distance} miles")

# Test 2: Airport data
print("\n2. Testing Airport Data:")
print("-" * 60)
print(f"Total airports: {len(AIRPORT_DATA)}")
print(f"Indian airports: {len([k for k in AIRPORT_DATA.keys() if k in ['DEL', 'BOM', 'BLR', 'MAA', 'HYD', 'CCU', 'AMD', 'PNQ', 'GOI', 'COK']])}")

# Test 3: Current time
print("\n3. Testing Real-Time Data:")
print("-" * 60)
now = datetime.now()
print(f"Current time: {now.strftime('%Y-%m-%d %H:%M')}")
print(f"Current hour: {now.hour}")
print(f"Current month: {now.month}")
print(f"Current day of week: {now.isoweekday()}")
print(f"Is peak hour: {now.hour in list(range(6, 10)) + list(range(16, 20))}")
print(f"Is weekend: {now.isoweekday() in [6, 7]}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
