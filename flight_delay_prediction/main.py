import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_preprocessing import DataPreprocessor
from src.weather_api import WeatherAPI, get_city_from_airport
from src.train_model import ModelTrainer
from src.predict_delay import FlightDelayPredictor, predict_with_weather
from src.visualization import FlightVisualizer

def train_mode():
    """Train the model using flight data"""
    print("\n" + "="*60)
    print("FLIGHT DELAY PREDICTION - TRAINING MODE")
    print("="*60)
    
    # Get dataset path
    data_path = input("\nEnter path to flight dataset CSV: ").strip()
    if not os.path.exists(data_path):
        print(f"Error: File not found - {data_path}")
        return
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load and prepare data
    print("\nLoading data...")
    df = preprocessor.load_data(data_path)
    if df is None:
        return
    
    print("\nPreprocessing data...")
    X_train, X_test, y_train, y_test, feature_names = preprocessor.prepare_data(df)
    
    # Train models
    trainer = ModelTrainer()
    results = trainer.train_all_models(X_train, y_train, X_test, y_test, feature_names)
    
    # Save model
    model_path = os.path.join('models', 'flight_delay_model.pkl')
    trainer.save_model(model_path, preprocessor)
    
    # Visualizations
    visualize = input("\nGenerate visualizations? (y/n): ").strip().lower()
    if visualize == 'y':
        visualizer = FlightVisualizer()
        df_processed = preprocessor.load_data(data_path)
        df_processed = preprocessor.clean_data(df_processed)
        df_processed = preprocessor.create_target(df_processed)
        df_processed = preprocessor.engineer_features(df_processed)
        
        visualizer.generate_all_visualizations(
            df_processed, 
            results, 
            trainer.get_feature_importance()
        )
    
    print("\n✓ Training complete!")

def predict_mode():
    """Predict flight delay"""
    print("\n" + "="*60)
    print("FLIGHT DELAY PREDICTION - PREDICTION MODE")
    print("="*60)
    
    # Check if model exists
    model_path = os.path.join('models', 'flight_delay_model.pkl')
    if not os.path.exists(model_path):
        print("\nError: Model not found. Please train the model first.")
        return
    
    # Get OpenWeather API key
    api_key = input("\nEnter OpenWeather API key (or press Enter to skip weather): ").strip()
    
    # Get flight information
    print("\n" + "-"*60)
    print("Enter Flight Information:")
    print("-"*60)
    
    origin = input("Departure Airport (e.g., ATL): ").strip().upper()
    destination = input("Destination Airport (e.g., LAX): ").strip().upper()
    airline = input("Airline Code (e.g., AA, DL, UA): ").strip().upper()
    
    # Get departure time
    dep_time_str = input("Scheduled Departure Time (HHMM, e.g., 1430): ").strip()
    try:
        dep_time = int(dep_time_str)
    except:
        dep_time = 1200
    
    # Get distance
    distance_str = input("Flight Distance (miles): ").strip()
    try:
        distance = int(distance_str)
    except:
        distance = 1000
    
    # Get date info
    month = int(input("Month (1-12): ").strip() or datetime.now().month)
    day_of_week = int(input("Day of Week (0=Mon, 6=Sun): ").strip() or datetime.now().weekday())
    
    # Prepare flight info
    flight_info = {
        'origin': origin,
        'destination': destination,
        'airline': airline,
        'departure_time': dep_time,
        'distance': distance,
        'month': month,
        'day_of_week': day_of_week
    }
    
    # Get weather data if API key provided
    weather_features = None
    if api_key:
        weather_api = WeatherAPI(api_key)
        city = get_city_from_airport(origin)
        print(f"\nFetching weather for {city}...")
        weather_data = weather_api.get_weather(city)
        weather_features = weather_api.extract_features(weather_data)
        weather_api.display_weather(weather_features)
    
    # Make prediction
    print("\nAnalyzing flight delay probability...")
    
    if weather_features:
        result = predict_with_weather(model_path, flight_info, weather_features)
        predictor = FlightDelayPredictor(model_path)
        predictor.display_prediction(result, weather_features)
    else:
        predictor = FlightDelayPredictor(model_path)
        result = predictor.predict(flight_info)
        predictor.display_prediction(result)

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("FLIGHT DELAY PREDICTION SYSTEM")
    print("="*60)
    print("\nSelect Mode:")
    print("1. Train Model")
    print("2. Predict Flight Delay")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        train_mode()
    elif choice == '2':
        predict_mode()
    elif choice == '3':
        print("\nGoodbye!")
        return
    else:
        print("\nInvalid choice!")
    
    # Ask to continue
    continue_choice = input("\nReturn to main menu? (y/n): ").strip().lower()
    if continue_choice == 'y':
        main()

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    main()
