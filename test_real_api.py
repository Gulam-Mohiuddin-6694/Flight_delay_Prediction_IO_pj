import sys
sys.path.append('src')
from flight_lookup import FlightLookup

print("Testing Real-Time Flight API")
print("=" * 60)

lookup = FlightLookup()
print(f"API Key: {lookup.aviationstack_key[:10]}...")

# Test with actual flight
test_flight = "AA100"
print(f"\nTesting: {test_flight}")

result = lookup.lookup_flight(test_flight)

if result['found']:
    print(f"\nSUCCESS!")
    print(f"Airline: {result['airline_name']}")
    print(f"Route: {result['origin']} -> {result['destination']}")
    print(f"Status: {result['status']}")
    print(f"Source: {result.get('source', 'unknown')}")
else:
    print(f"\nFailed: {result['error']}")

print("=" * 60)
