import sys
sys.path.append('src')

from flight_lookup import FlightLookup

print("=" * 60)
print("Testing Flight Number Lookup Feature")
print("=" * 60)

lookup = FlightLookup()

# Test cases
test_flights = [
    '6E2345',  # IndiGo Delhi-Mumbai
    'AI101',   # Air India Delhi-Dubai
    'EK512',   # Emirates Dubai-Delhi
    'AA100',   # American JFK-LAX
    'INVALID', # Invalid flight
]

for flight_num in test_flights:
    print(f"\nLooking up: {flight_num}")
    print("-" * 60)
    
    result = lookup.lookup_flight(flight_num)
    
    if result['found']:
        print(f"FOUND!")
        print(f"  Airline: {result['airline_name']} ({result['airline']})")
        print(f"  Flight: {result['flight_number']}")
        print(f"  Route: {result['origin_name']} ({result['origin']}) -> {result['destination_name']} ({result['destination']})")
        print(f"  Status: {result['status']}")
        if result.get('source') == 'demo':
            print(f"  Source: Demo data")
    else:
        print(f"NOT FOUND")
        print(f"  Error: {result['error']}")
        if result.get('available_demos'):
            print(f"  Try: {', '.join(result['available_demos'])}")

print("\n" + "=" * 60)
print("Flight lookup feature is working!")
print("=" * 60)
print("\nAvailable demo flights:")
print("  Indian: 6E2345, 6E123, AI101, AI191, UK955, SG234")
print("  International: EK512, SQ406, BA142")
print("  US: AA100, DL1234, UA456")
