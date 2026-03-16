import sys
import os
sys.path.append('src')

from flight_lookup import FlightLookup

print("=" * 70)
print("FLIGHT API DIAGNOSTIC TEST")
print("=" * 70)

# Check environment variable
api_key = os.getenv('AVIATIONSTACK_API_KEY')
print(f"\n1. Checking API Key:")
print("-" * 70)
if api_key:
    print(f"   API Key Found: {api_key[:10]}...{api_key[-4:]}")
    print(f"   Length: {len(api_key)} characters")
else:
    print("   API Key NOT SET in environment")
    print("   To set it, run:")
    print("   set AVIATIONSTACK_API_KEY=your_key_here")

# Initialize lookup
print(f"\n2. Initializing Flight Lookup:")
print("-" * 70)
lookup = FlightLookup()
print(f"   Stored API Key: {lookup.aviationstack_key[:10] if lookup.aviationstack_key != 'demo_key' else 'demo_key'}...")

# Test with a real flight number
print(f"\n3. Testing Flight Lookup:")
print("-" * 70)

test_flight = "6E2345"  # IndiGo flight
print(f"   Testing with: {test_flight}")
print()

result = lookup.lookup_flight(test_flight)

print(f"\n4. Result:")
print("-" * 70)
if result['found']:
    print(f"   Status: FOUND")
    print(f"   Airline: {result['airline_name']} ({result['airline']})")
    print(f"   Flight: {result['flight_number']}")
    print(f"   Route: {result['origin_name']} ({result['origin']}) -> {result['destination_name']} ({result['destination']})")
    print(f"   Status: {result['status']}")
    print(f"   Source: {result.get('source', 'unknown')}")
else:
    print(f"   Status: NOT FOUND")
    print(f"   Error: {result.get('error', 'Unknown error')}")

print("\n" + "=" * 70)
print("DIAGNOSIS:")
print("=" * 70)

if api_key and api_key != 'demo_key':
    print("✅ API Key is set")
    if result.get('source') == 'api':
        print("✅ Using REAL API data")
        print("\n🎉 SUCCESS! Real-time flight data is working!")
    else:
        print("❌ API call failed, using demo data")
        print("\nPossible issues:")
        print("1. API key might be invalid")
        print("2. Flight might not be active today")
        print("3. API rate limit reached")
        print("4. Network/firewall blocking API")
        print("\nTo verify API key:")
        print("Visit: https://aviationstack.com/dashboard")
else:
    print("❌ API Key NOT set")
    print("\n📝 To enable real-time data:")
    print("1. Get free API key from: https://aviationstack.com/")
    print("2. Run: set AVIATIONSTACK_API_KEY=your_key_here")
    print("3. Restart this test")
    print("\n✅ Demo mode is working fine for presentation!")

print("=" * 70)
