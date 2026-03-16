"""
Quick Start Guide for Flight Delay Prediction App
==================================================

Follow these steps to get your application running:
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║     Flight Delay Prediction - Quick Start Guide             ║
╚══════════════════════════════════════════════════════════════╝

📋 STEP 1: Install Dependencies
--------------------------------
Run: pip install -r requirements.txt

📥 STEP 2: Download Dataset
----------------------------
1. Visit: https://www.kaggle.com/datasets/usdot/flight-delays
2. Download the flights.csv file
3. Place it in the 'data/' folder

🔑 STEP 3: Get OpenWeather API Key
-----------------------------------
1. Sign up at: https://openweathermap.org/api
2. Get your free API key
3. Set environment variable:
   
   Windows:
   set OPENWEATHER_API_KEY=your_api_key_here
   
   Linux/Mac:
   export OPENWEATHER_API_KEY=your_api_key_here

   Or edit src/weather_api.py and replace YOUR_API_KEY_HERE

✅ STEP 4: Verify Dataset
--------------------------
Run: python verify_dataset.py

🤖 STEP 5: Train the Model
---------------------------
Run: cd src && python train_model.py

This will take a few minutes depending on dataset size.

🚀 STEP 6: Start the Application
---------------------------------
Run: python app.py

Then open: http://localhost:5000

📊 STEP 7: Use the Application
-------------------------------
1. Fill in flight details on the home page
2. Click "Predict Delay"
3. View results with weather information
4. Check the Analytics page for insights

═══════════════════════════════════════════════════════════════

💡 Tips:
--------
- Use a dataset with at least 10,000 rows for better accuracy
- The first prediction may take a few seconds (weather API call)
- Generate charts in Analytics page after training

🐛 Troubleshooting:
-------------------
- Model not loading? Run train_model.py first
- Weather API error? Check your API key
- Dataset error? Verify flights.csv exists in data/ folder

📚 For detailed documentation, see README.md

═══════════════════════════════════════════════════════════════
""")

# Check current status
import os

print("\n🔍 Current Status Check:")
print("-" * 60)

# Check if venv exists
if os.path.exists('venv') or os.path.exists('env'):
    print("✅ Virtual environment found")
else:
    print("❌ Virtual environment not found - create one first")

# Check if dataset exists
if os.path.exists('data/flights.csv'):
    print("✅ Dataset found (data/flights.csv)")
else:
    print("❌ Dataset not found - download and place in data/ folder")

# Check if model exists
if os.path.exists('models/delay_model.pkl'):
    print("✅ Trained model found")
else:
    print("❌ Model not trained - run train_model.py")

# Check if requirements are installed
try:
    import flask
    import pandas
    import sklearn
    print("✅ Dependencies installed")
except ImportError:
    print("❌ Dependencies not installed - run: pip install -r requirements.txt")

print("-" * 60)
print("\n🎯 Next Step: Follow the guide above to complete setup\n")
