# Configuration File
# ===================
# Copy this file to config.py and add your actual values

import os
from dotenv import load_dotenv

load_dotenv()

# OpenWeather API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Get your free API key from: https://openweathermap.org/api
# Free tier includes: 60 calls/minute, 1,000,000 calls/month

# Model Configuration
DELAY_THRESHOLD = 15  # Minutes - flights delayed more than this are classified as delayed
TRAIN_TEST_SPLIT = 0.2  # 80% training, 20% testing

# Flask Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Feature Engineering
PEAK_HOURS = [6, 7, 8, 9, 16, 17, 18, 19]  # Morning and evening rush hours
WEEKEND_DAYS = [6, 7]  # Saturday and Sunday

# Model Selection Criteria
MODEL_SELECTION_METRIC = 'f1'  # Options: 'accuracy', 'precision', 'recall', 'f1'
