import numpy as np
import joblib
from datetime import datetime

class FlightDelayPredictor:
    def __init__(self, model_path):
        self.model_data = joblib.load(model_path)
        self.model = self.model_data['model']
        self.model_name = self.model_data['model_name']
        self.feature_names = self.model_data['feature_names']
        self.preprocessor = self.model_data.get('preprocessor')
        print(f"Loaded model: {self.model_name}")
    
    def prepare_input(self, flight_info):
        """Prepare input features for prediction"""
        features = {}
        
        # Extract basic features
        features['MONTH'] = flight_info.get('month', datetime.now().month)
        features['DAY_OF_WEEK'] = flight_info.get('day_of_week', datetime.now().weekday())
        features['DISTANCE'] = flight_info.get('distance', 1000)
        
        # Time features
        dep_time = flight_info.get('departure_time', 1200)
        features['CRS_DEP_TIME'] = dep_time
        features['HOUR'] = dep_time // 100
        features['PEAK_HOUR'] = 1 if (6 <= features['HOUR'] <= 9) or (16 <= features['HOUR'] <= 19) else 0
        features['IS_WEEKEND'] = 1 if features['DAY_OF_WEEK'] >= 5 else 0
        
        # Encode categorical features
        if self.preprocessor:
            # Origin airport
            origin = flight_info.get('origin', 'ATL')
            if 'ORIGIN' in self.preprocessor.label_encoders:
                try:
                    features['ORIGIN'] = self.preprocessor.label_encoders['ORIGIN'].transform([origin])[0]
                except:
                    features['ORIGIN'] = 0
            
            # Destination airport
            dest = flight_info.get('destination', 'LAX')
            if 'DEST' in self.preprocessor.label_encoders:
                try:
                    features['DEST'] = self.preprocessor.label_encoders['DEST'].transform([dest])[0]
                except:
                    features['DEST'] = 0
            
            # Airline
            airline = flight_info.get('airline', 'AA')
            if 'OP_CARRIER' in self.preprocessor.label_encoders:
                try:
                    features['OP_CARRIER'] = self.preprocessor.label_encoders['OP_CARRIER'].transform([airline])[0]
                except:
                    features['OP_CARRIER'] = 0
            elif 'AIRLINE' in self.preprocessor.label_encoders:
                try:
                    features['AIRLINE'] = self.preprocessor.label_encoders['AIRLINE'].transform([airline])[0]
                except:
                    features['AIRLINE'] = 0
        
        # Create feature vector in correct order
        feature_vector = []
        for feature_name in self.feature_names:
            feature_vector.append(features.get(feature_name, 0))
        
        return np.array(feature_vector).reshape(1, -1)
    
    def predict(self, flight_info):
        """Predict flight delay"""
        # Prepare input
        X = self.prepare_input(flight_info)
        
        # Scale features if preprocessor available
        if self.preprocessor and hasattr(self.preprocessor, 'scaler'):
            X = self.preprocessor.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        
        # Get probability
        if hasattr(self.model, 'predict_proba'):
            probability = self.model.predict_proba(X)[0]
            delay_probability = probability[1] * 100
        else:
            delay_probability = 50.0 if prediction == 1 else 10.0
        
        return {
            'prediction': prediction,
            'delay_probability': delay_probability,
            'status': 'Likely Delayed' if prediction == 1 else 'On Time'
        }
    
    def display_prediction(self, result, weather_info=None):
        """Display prediction results"""
        print("\n" + "="*50)
        print("PREDICTION RESULT")
        print("="*50)
        
        if weather_info:
            print(f"Weather Condition: {weather_info.get('weather_description', 'N/A').title()}")
            print(f"Wind Speed: {weather_info.get('wind_speed', 0):.1f} m/s")
            print(f"Weather Severity: {weather_info.get('weather_severity', 0)}/10")
            print("-"*50)
        
        print(f"Flight Delay Probability: {result['delay_probability']:.1f}%")
        print(f"Status: {result['status']}")
        
        if result['delay_probability'] > 70:
            print("\n⚠️  HIGH RISK OF DELAY")
        elif result['delay_probability'] > 40:
            print("\n⚠️  MODERATE RISK OF DELAY")
        else:
            print("\n✓ LOW RISK OF DELAY")
        
        print("="*50 + "\n")

def predict_with_weather(model_path, flight_info, weather_features):
    """Make prediction incorporating weather data"""
    predictor = FlightDelayPredictor(model_path)
    
    # Add weather severity to flight info
    flight_info['weather_severity'] = weather_features.get('weather_severity', 0)
    
    # Make prediction
    result = predictor.predict(flight_info)
    
    # Adjust probability based on weather severity
    weather_impact = weather_features.get('weather_severity', 0) * 3
    result['delay_probability'] = min(result['delay_probability'] + weather_impact, 99.0)
    
    # Update status based on adjusted probability
    if result['delay_probability'] > 50:
        result['prediction'] = 1
        result['status'] = 'Likely Delayed'
    
    return result
