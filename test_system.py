"""
System Test Script
==================

This script tests all components of the Flight Delay Prediction system.
"""

import os
import sys

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n1️⃣  Testing Dependencies...")
    print("-" * 60)
    
    required_packages = {
        'flask': 'Flask',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'requests': 'requests',
        'joblib': 'joblib',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def test_file_structure():
    """Test if all required files and folders exist"""
    print("\n2️⃣  Testing File Structure...")
    print("-" * 60)
    
    required_paths = {
        'data': 'Data folder',
        'models': 'Models folder',
        'static': 'Static folder',
        'static/css': 'CSS folder',
        'static/js': 'JavaScript folder',
        'templates': 'Templates folder',
        'src': 'Source code folder',
        'src/data_preprocessing.py': 'Data preprocessing module',
        'src/train_model.py': 'Model training script',
        'src/weather_api.py': 'Weather API module',
        'src/predict.py': 'Prediction module',
        'app.py': 'Flask application',
        'requirements.txt': 'Requirements file',
        'README.md': 'Documentation'
    }
    
    all_exist = True
    for path, description in required_paths.items():
        if os.path.exists(path):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_dataset():
    """Test if dataset exists and is valid"""
    print("\n3️⃣  Testing Dataset...")
    print("-" * 60)
    
    dataset_path = 'data/flights.csv'
    
    if not os.path.exists(dataset_path):
        print(f"   ❌ Dataset not found at {dataset_path}")
        print("   💡 Run: python generate_sample_data.py")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(dataset_path, nrows=10)
        print(f"   ✅ Dataset loaded successfully")
        print(f"   📊 Columns: {len(df.columns)}")
        print(f"   📝 Sample columns: {', '.join(list(df.columns)[:5])}")
        return True
    except Exception as e:
        print(f"   ❌ Error loading dataset: {str(e)}")
        return False

def test_model():
    """Test if trained model exists"""
    print("\n4️⃣  Testing Trained Model...")
    print("-" * 60)
    
    model_files = {
        'models/delay_model.pkl': 'Trained model',
        'models/preprocessor.pkl': 'Preprocessor',
        'models/feature_columns.pkl': 'Feature columns'
    }
    
    all_exist = True
    for path, description in model_files.items():
        if os.path.exists(path):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("   💡 Run: cd src && python train_model.py")
    
    return all_exist

def test_weather_api():
    """Test weather API connection"""
    print("\n5️⃣  Testing Weather API...")
    print("-" * 60)
    
    try:
        sys.path.append('src')
        from weather_api import WeatherAPI
        
        api = WeatherAPI()
        
        # Test with a sample city
        weather = api.get_weather('New York')
        
        if weather:
            print(f"   ✅ Weather API connection successful")
            print(f"   🌡️  Temperature: {weather['main']['temp']}°C")
            print(f"   💨 Wind Speed: {weather['wind']['speed']} m/s")
            return True
        else:
            print(f"   ⚠️  Weather API returned no data")
            print(f"   💡 Check your API key in src/weather_api.py")
            return False
            
    except Exception as e:
        print(f"   ❌ Weather API error: {str(e)}")
        print(f"   💡 Set OPENWEATHER_API_KEY environment variable")
        return False

def test_prediction():
    """Test prediction functionality"""
    print("\n6️⃣  Testing Prediction System...")
    print("-" * 60)
    
    if not os.path.exists('models/delay_model.pkl'):
        print("   ⚠️  Model not trained yet - skipping prediction test")
        return False
    
    try:
        sys.path.append('src')
        from predict import FlightDelayPredictor
        
        predictor = FlightDelayPredictor()
        predictor.load_model()
        predictor.load_preprocessor()
        predictor.load_feature_columns()
        
        print("   ✅ Prediction system loaded successfully")
        
        # Test prediction
        test_data = {
            'OP_CARRIER': 'AA',
            'ORIGIN': 'JFK',
            'DEST': 'LAX',
            'DISTANCE': 2475,
            'MONTH': 7,
            'DAY_OF_WEEK': 3,
            'HOUR': 14,
            'IS_PEAK_HOUR': 0,
            'IS_WEEKEND': 0
        }
        
        result = predictor.predict(test_data, 'JFK')
        print(f"   ✅ Test prediction successful")
        print(f"   📊 Delay Probability: {result['probability']:.2f}%")
        print(f"   🎯 Status: {result['status']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Prediction error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Flight Delay Prediction - System Test")
    print("=" * 60)
    
    results = {
        'Dependencies': test_dependencies(),
        'File Structure': test_file_structure(),
        'Dataset': test_dataset(),
        'Trained Model': test_model(),
        'Weather API': test_weather_api(),
        'Prediction': test_prediction()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
        print("🚀 Run: python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("📚 See README.md for detailed setup instructions")
    print("=" * 60)

if __name__ == "__main__":
    main()
