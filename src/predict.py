import pandas as pd
import numpy as np
import joblib
from weather_api import WeatherAPI, get_city_from_airport

class FlightDelayPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_columns = None
        self.weather_api = WeatherAPI()
        
    def load_model(self, model_path='models/delay_model.pkl'):
        """Load trained model"""
        self.model = joblib.load(model_path)
        print("Model loaded successfully")
    
    def load_preprocessor(self, preprocessor_path='models/preprocessor.pkl'):
        """Load preprocessor"""
        data = joblib.load(preprocessor_path)
        self.preprocessor = data
        print("Preprocessor loaded successfully")
    
    def load_feature_columns(self, feature_path='models/feature_columns.pkl'):
        """Load feature columns"""
        self.feature_columns = joblib.load(feature_path)
        print("Feature columns loaded successfully")
    
    def prepare_input(self, flight_data, weather_features):
        """Prepare input data for prediction"""
        # Combine flight data and weather features
        input_data = {**flight_data, **weather_features}
        
        # Create DataFrame
        df = pd.DataFrame([input_data])
        
        # Encode categorical variables
        for col, encoder in self.preprocessor['label_encoders'].items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col].astype(str))
                except ValueError:
                    # Handle unseen categories
                    df[col] = 0
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Select and order features
        df = df[self.feature_columns]
        
        # Scale features
        scaled_data = self.preprocessor['scaler'].transform(df)
        
        return scaled_data
    
    def predict(self, flight_data, origin_airport):
        """Make prediction with weather data"""
        # Get weather data
        city = get_city_from_airport(origin_airport)
        weather_data = self.weather_api.get_weather(city)
        weather_features = self.weather_api.extract_weather_features(weather_data)
        
        # Prepare input
        input_data = self.prepare_input(flight_data, weather_features)
        
        # Make prediction
        prediction = self.model.predict(input_data)[0]
        probability = self.model.predict_proba(input_data)[0]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability[1] * 100),
            'weather': weather_features,
            'status': 'Likely Delayed' if prediction == 1 else 'On Time'
        }
