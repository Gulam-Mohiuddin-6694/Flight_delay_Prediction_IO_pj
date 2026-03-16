from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.enhanced_predict import EnhancedFlightDelayPredictor
from src.flight_lookup import FlightLookup
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Initialize predictor and flight lookup
predictor = EnhancedFlightDelayPredictor()
flight_lookup = FlightLookup()

try:
    predictor.load_model()
    predictor.load_preprocessor()
    predictor.load_feature_columns()
    predictor.load_historical_data()
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model_loaded = False

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/lookup-flight', methods=['POST'])
def lookup_flight_route():
    """Flight number lookup endpoint"""
    try:
        flight_number = request.json.get('flight_number', '').strip()
        result = flight_lookup.lookup_flight(flight_number)
        return jsonify(result)
    except Exception as e:
        return jsonify({'found': False, 'error': str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
    
    try:
        from datetime import datetime
        from src.weather_api import calculate_distance
        
        # Get form data
        data = request.form
        
        origin = data.get('origin')
        destination = data.get('destination')
        
        # Auto-calculate distance
        distance = calculate_distance(origin, destination)
        
        # Get current date/time
        now = datetime.now()
        current_hour = now.hour
        current_month = now.month
        current_day_of_week = now.isoweekday()  # 1=Monday, 7=Sunday
        
        flight_data = {
            'OP_CARRIER': data.get('airline'),
            'ORIGIN': origin,
            'DEST': destination,
            'DISTANCE': float(distance),
            'MONTH': current_month,
            'DAY_OF_WEEK': current_day_of_week,
            'HOUR': current_hour,
            'IS_PEAK_HOUR': 1 if current_hour in list(range(6, 10)) + list(range(16, 20)) else 0,
            'IS_WEEKEND': 1 if current_day_of_week in [6, 7] else 0
        }
        
        # Make prediction
        result = predictor.predict(flight_data, origin)
        result['distance'] = distance
        result['current_time'] = now.strftime('%Y-%m-%d %H:%M')
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    return render_template('analytics.html')

@app.route('/api/analytics-data')
def analytics_data():
    """Get analytics data"""
    try:
        df = pd.read_csv('data/flights.csv')
        
        # Sample data for performance
        if len(df) > 10000:
            df = df.sample(10000)
        
        # Calculate statistics
        stats = {
            'total_flights': len(df),
            'delayed_flights': len(df[df.get('DEP_DELAY', df.get('DEPARTURE_DELAY', pd.Series([0]))).fillna(0) > 15]),
            'delay_rate': 0
        }
        
        if stats['total_flights'] > 0:
            stats['delay_rate'] = round((stats['delayed_flights'] / stats['total_flights']) * 100, 2)
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/generate-charts')
def generate_charts():
    """Generate analytics charts"""
    try:
        df = pd.read_csv('data/flights.csv')
        
        # Sample for performance
        if len(df) > 10000:
            df = df.sample(10000)
        
        # Delay distribution
        plt.figure(figsize=(10, 6))
        delay_col = 'DEP_DELAY' if 'DEP_DELAY' in df.columns else 'DEPARTURE_DELAY'
        if delay_col in df.columns:
            df[delay_col].fillna(0).hist(bins=50)
            plt.title('Flight Delay Distribution')
            plt.xlabel('Delay (minutes)')
            plt.ylabel('Frequency')
            plt.savefig('static/delay_distribution.png')
            plt.close()
        
        # Delays by airline
        plt.figure(figsize=(12, 6))
        carrier_col = 'OP_CARRIER' if 'OP_CARRIER' in df.columns else 'AIRLINE'
        if carrier_col in df.columns and delay_col in df.columns:
            delay_by_carrier = df.groupby(carrier_col)[delay_col].mean().sort_values(ascending=False).head(10)
            delay_by_carrier.plot(kind='bar')
            plt.title('Average Delay by Airline (Top 10)')
            plt.xlabel('Airline')
            plt.ylabel('Average Delay (minutes)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('static/delay_by_airline.png')
            plt.close()
        
        # Delays by month
        plt.figure(figsize=(10, 6))
        if 'MONTH' in df.columns and delay_col in df.columns:
            delay_by_month = df.groupby('MONTH')[delay_col].mean()
            delay_by_month.plot(kind='line', marker='o')
            plt.title('Average Delay by Month')
            plt.xlabel('Month')
            plt.ylabel('Average Delay (minutes)')
            plt.grid(True)
            plt.savefig('static/delay_by_month.png')
            plt.close()
        
        return jsonify({'status': 'Charts generated successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
