import sys
sys.path.append('src')

from enhanced_predict import EnhancedFlightDelayPredictor
from datetime import datetime

print("=" * 60)
print("Testing Enhanced Prediction System")
print("=" * 60)

# Initialize predictor
predictor = EnhancedFlightDelayPredictor()
predictor.load_model()
predictor.load_preprocessor()
predictor.load_feature_columns()
predictor.load_historical_data()

# Test cases
test_flights = [
    {
        'name': 'Delhi to Mumbai (IndiGo)',
        'data': {
            'OP_CARRIER': '6E',
            'ORIGIN': 'DEL',
            'DEST': 'BOM',
            'DISTANCE': 706.58,
            'MONTH': datetime.now().month,
            'DAY_OF_WEEK': datetime.now().isoweekday(),
            'HOUR': datetime.now().hour,
            'IS_PEAK_HOUR': 1 if datetime.now().hour in list(range(6, 10)) + list(range(16, 20)) else 0,
            'IS_WEEKEND': 1 if datetime.now().isoweekday() in [6, 7] else 0
        }
    },
    {
        'name': 'New York to Los Angeles (American)',
        'data': {
            'OP_CARRIER': 'AA',
            'ORIGIN': 'JFK',
            'DEST': 'LAX',
            'DISTANCE': 2469.69,
            'MONTH': datetime.now().month,
            'DAY_OF_WEEK': datetime.now().isoweekday(),
            'HOUR': datetime.now().hour,
            'IS_PEAK_HOUR': 1 if datetime.now().hour in list(range(6, 10)) + list(range(16, 20)) else 0,
            'IS_WEEKEND': 1 if datetime.now().isoweekday() in [6, 7] else 0
        }
    }
]

for test in test_flights:
    print(f"\nTest: {test['name']}")
    print("-" * 60)
    
    try:
        result = predictor.predict(test['data'], test['data']['ORIGIN'])
        
        print(f"Delay Probability: {result['probability']:.2f}%")
        print(f"Status: {result['status']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        
        if result['route_history']:
            print(f"\nRoute History:")
            print(f"  Total Flights: {result['route_history']['total_flights']}")
            print(f"  Avg Delay: {result['route_history']['avg_delay']:.1f} min")
            print(f"  On-Time Rate: {result['route_history']['on_time_rate']:.1f}%")
        
        if result['alternatives']:
            print(f"\nAlternative Routes:")
            for alt in result['alternatives']:
                print(f"  - {alt['route']} ({alt['total_distance']} miles)")
        
        print(f"\nWeather:")
        print(f"  Temperature: {result['weather']['temperature']:.1f}C")
        print(f"  Severity: {result['weather']['weather_severity']}/10")
        
        print("\nOK - Prediction successful")
        
    except Exception as e:
        print(f"ERROR - {str(e)}")

print("\n" + "=" * 60)
print("All prediction tests completed!")
print("=" * 60)
