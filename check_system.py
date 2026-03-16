import os
import sys

def test_files():
    """Test if all required files exist"""
    print("\n1. Testing File Structure...")
    print("-" * 60)
    
    required_files = {
        'data/flights.csv': 'Dataset',
        'models/delay_model.pkl': 'Trained model',
        'models/preprocessor.pkl': 'Preprocessor',
        'models/feature_columns.pkl': 'Feature columns',
        'src/enhanced_predict.py': 'Enhanced predictor',
        'src/weather_api.py': 'Weather API',
        'app.py': 'Flask app',
        'templates/index.html': 'Main page',
        'static/css/style.css': 'Stylesheet',
        'static/js/script.js': 'JavaScript'
    }
    
    all_exist = True
    for path, description in required_files.items():
        if os.path.exists(path):
            print(f"   OK - {description}")
        else:
            print(f"   MISSING - {description}")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if all modules can be imported"""
    print("\n2. Testing Python Imports...")
    print("-" * 60)
    
    modules = ['flask', 'pandas', 'numpy', 'sklearn', 'requests', 'joblib', 'matplotlib', 'seaborn']
    
    all_imported = True
    for module in modules:
        try:
            __import__(module)
            print(f"   OK - {module}")
        except ImportError:
            print(f"   MISSING - {module}")
            all_imported = False
    
    return all_imported

def test_enhanced_predictor():
    """Test enhanced predictor"""
    print("\n3. Testing Enhanced Predictor...")
    print("-" * 60)
    
    try:
        sys.path.append('src')
        from enhanced_predict import EnhancedFlightDelayPredictor
        
        predictor = EnhancedFlightDelayPredictor()
        predictor.load_model()
        predictor.load_preprocessor()
        predictor.load_feature_columns()
        predictor.load_historical_data()
        
        print("   OK - Enhanced predictor loaded")
        return True
    except Exception as e:
        print(f"   ERROR - {str(e)}")
        return False

def test_distance_calculation():
    """Test distance calculation"""
    print("\n4. Testing Distance Calculation...")
    print("-" * 60)
    
    try:
        sys.path.append('src')
        from weather_api import calculate_distance
        
        test_routes = [
            ('DEL', 'BOM', 706.58),
            ('JFK', 'LAX', 2469.69),
            ('BLR', 'DEL', 1061.89)
        ]
        
        all_ok = True
        for origin, dest, expected in test_routes:
            distance = calculate_distance(origin, dest)
            if abs(distance - expected) < 10:
                print(f"   OK - {origin} to {dest}: {distance} miles")
            else:
                print(f"   ERROR - {origin} to {dest}: Expected {expected}, got {distance}")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"   ERROR - {str(e)}")
        return False

def test_dataset():
    """Test dataset"""
    print("\n5. Testing Dataset...")
    print("-" * 60)
    
    try:
        import pandas as pd
        df = pd.read_csv('data/flights.csv')
        
        print(f"   OK - Dataset loaded")
        print(f"   Records: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Airlines: {df['OP_CARRIER'].nunique()}")
        print(f"   Airports: {df['ORIGIN'].nunique()}")
        
        return True
    except Exception as e:
        print(f"   ERROR - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Flight Delay Prediction - System Test")
    print("=" * 60)
    
    results = {
        'Files': test_files(),
        'Imports': test_imports(),
        'Enhanced Predictor': test_enhanced_predictor(),
        'Distance Calculation': test_distance_calculation(),
        'Dataset': test_dataset()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! System is ready.")
        print("Run: python app.py")
    else:
        print("Some tests failed. Check errors above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
