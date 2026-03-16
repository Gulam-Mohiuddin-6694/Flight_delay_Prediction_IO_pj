import pandas as pd
import numpy as np
import joblib
from weather_api import WeatherAPI, get_city_from_airport, calculate_distance

class EnhancedFlightDelayPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_columns = None
        self.weather_api = WeatherAPI()
        self.historical_data = None
        
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
    
    def load_historical_data(self, data_path='data/flights.csv'):
        """Load historical data for analysis"""
        try:
            self.historical_data = pd.read_csv(data_path)
            print("Historical data loaded")
        except:
            print("Historical data not available")
    
    def prepare_input(self, flight_data, weather_features):
        """Prepare input data for prediction"""
        input_data = {**flight_data, **weather_features}
        df = pd.DataFrame([input_data])
        
        for col, encoder in self.preprocessor['label_encoders'].items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col].astype(str))
                except ValueError:
                    df[col] = 0
        
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        df = df[self.feature_columns]
        scaled_data = self.preprocessor['scaler'].transform(df)
        
        return scaled_data
    
    def calculate_confidence(self, probabilities):
        """Calculate prediction confidence score"""
        max_prob = max(probabilities[0])
        confidence = (max_prob - 0.5) * 200  # Scale to 0-100
        return max(0, min(100, confidence))
    
    def get_route_history(self, origin, destination):
        """Get historical delay statistics for route"""
        if self.historical_data is None:
            return None
        
        route_data = self.historical_data[
            (self.historical_data['ORIGIN'] == origin) & 
            (self.historical_data['DEST'] == destination)
        ]
        
        if len(route_data) == 0:
            return None
        
        return {
            'total_flights': len(route_data),
            'avg_delay': route_data['DEP_DELAY'].mean(),
            'max_delay': route_data['DEP_DELAY'].max(),
            'on_time_rate': (route_data['DEP_DELAY'] <= 15).sum() / len(route_data) * 100
        }
    
    def suggest_alternatives(self, origin, destination, current_probability):
        """Suggest alternative routes if delay probability is high"""
        if current_probability < 60:
            return []
        
        # Common hub airports
        hubs = ['ATL', 'ORD', 'DFW', 'DEN', 'DXB', 'SIN', 'DEL', 'BOM']
        alternatives = []
        
        for hub in hubs:
            if hub != origin and hub != destination:
                dist1 = calculate_distance(origin, hub)
                dist2 = calculate_distance(hub, destination)
                total_dist = dist1 + dist2
                direct_dist = calculate_distance(origin, destination)
                
                # Only suggest if not too much longer
                if total_dist < direct_dist * 1.5:
                    alternatives.append({
                        'route': f"{origin} → {hub} → {destination}",
                        'hub': hub,
                        'total_distance': round(total_dist, 0)
                    })
        
        return alternatives[:3]  # Return top 3
    
    def predict(self, flight_data, origin_airport):
        """Enhanced prediction with additional insights"""
        # Get weather data
        city = get_city_from_airport(origin_airport)
        weather_data = self.weather_api.get_weather(city)
        weather_features = self.weather_api.extract_weather_features(weather_data)
        
        # Prepare input
        input_data = self.prepare_input(flight_data, weather_features)
        
        # Make prediction
        prediction = self.model.predict(input_data)[0]
        probabilities = self.model.predict_proba(input_data)
        probability = float(probabilities[0][1] * 100)
        
        # Calculate confidence
        confidence = self.calculate_confidence(probabilities)
        
        # Get route history
        route_history = self.get_route_history(
            flight_data['ORIGIN'], 
            flight_data['DEST']
        )
        
        # Suggest alternatives if high delay probability
        alternatives = self.suggest_alternatives(
            flight_data['ORIGIN'],
            flight_data['DEST'],
            probability
        )
        
        # Determine risk level
        if probability < 30:
            risk_level = 'Low'
            risk_color = '#51cf66'
        elif probability < 60:
            risk_level = 'Medium'
            risk_color = '#ffa94d'
        else:
            risk_level = 'High'
            risk_color = '#ff6b6b'
        
        return {
            'prediction': int(prediction),
            'probability': probability,
            'confidence': confidence,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'weather': weather_features,
            'status': 'Likely Delayed' if prediction == 1 else 'On Time',
            'route_history': route_history,
            'alternatives': alternatives
        }
