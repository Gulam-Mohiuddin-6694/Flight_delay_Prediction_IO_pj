# Complete Setup Guide

## Quick Start (Windows)

### Option 1: Automated Setup (Recommended)

Simply run the setup script:

```bash
setup.bat
```

This will automatically:
- Create virtual environment
- Install all dependencies
- Generate sample dataset
- Train the machine learning model

Then start the application:

```bash
start.bat
```

### Option 2: Manual Setup

Follow the detailed steps below.

---

## Detailed Manual Setup

### Step 1: Prerequisites

Ensure you have installed:
- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (optional) - [Download](https://git-scm.com/)

Verify installation:
```bash
python --version
pip --version
```

### Step 2: Create Virtual Environment

```bash
# Navigate to project directory
cd flight-delay-webapp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- pandas & numpy (data processing)
- scikit-learn (machine learning)
- matplotlib & seaborn (visualization)
- requests (API calls)
- And more...

### Step 4: Get Dataset

#### Option A: Generate Sample Data (Quick Testing)

```bash
python generate_sample_data.py
```

This creates a synthetic dataset with 50,000 flight records.

#### Option B: Download Real Data from Kaggle (Recommended for Production)

1. **Create Kaggle Account**
   - Go to [kaggle.com](https://www.kaggle.com)
   - Sign up for free account

2. **Download Dataset**
   - Visit: [Flight Delays Dataset](https://www.kaggle.com/datasets/usdot/flight-delays)
   - Click "Download" button
   - Extract the ZIP file

3. **Place Dataset**
   - Copy `flights.csv` to `data/` folder
   - Or rename your CSV file to `flights.csv`

4. **Verify Dataset**
   ```bash
   python verify_dataset.py
   ```

### Step 5: Get OpenWeather API Key

1. **Sign Up**
   - Go to [OpenWeather](https://openweathermap.org/api)
   - Click "Sign Up" (free account)
   - Verify your email

2. **Get API Key**
   - Log in to your account
   - Go to "API keys" section
   - Copy your API key

3. **Set API Key**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENWEATHER_API_KEY=your_api_key_here

   # Windows (PowerShell)
   $env:OPENWEATHER_API_KEY="your_api_key_here"

   # Linux/Mac
   export OPENWEATHER_API_KEY=your_api_key_here
   ```

   **Option B: Edit Code**
   - Open `src/weather_api.py`
   - Find line: `self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')`
   - Replace `YOUR_API_KEY_HERE` with your actual key

### Step 6: Train the Model

```bash
cd src
python train_model.py
```

This process will:
1. Load the dataset
2. Clean and preprocess data
3. Create features
4. Train 3 different models
5. Compare performance
6. Save the best model

**Expected Output:**
```
Loading dataset...
Loaded 50000 records
Removed 0 rows with missing values

Training set: 40000 samples
Test set: 10000 samples

Training Logistic Regression...
Logistic Regression Results:
Accuracy: 0.7823
Precision: 0.7456
Recall: 0.7234
F1 Score: 0.7343

Training Random Forest...
Random Forest Results:
Accuracy: 0.8234
Precision: 0.8012
Recall: 0.7845
F1 Score: 0.7927

Training Gradient Boosting...
Gradient Boosting Results:
Accuracy: 0.8456
Precision: 0.8234
Recall: 0.8123
F1 Score: 0.8178

Best Model: Gradient Boosting
Best model saved to models/delay_model.pkl
```

**Time Required**: 2-10 minutes (depends on dataset size)

### Step 7: Test the System

```bash
cd ..
python test_system.py
```

This verifies:
- All dependencies installed
- File structure correct
- Dataset loaded
- Model trained
- Weather API working
- Prediction system functional

### Step 8: Start the Application

```bash
python app.py
```

**Expected Output:**
```
Model loaded successfully
Preprocessor loaded successfully
Feature columns loaded successfully
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 9: Access the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the Flight Delay Prediction interface

---

## Using the Application

### Making Predictions

1. **Fill in Flight Details**
   - Select airline (e.g., American Airlines)
   - Choose origin airport (e.g., JFK)
   - Choose destination airport (e.g., LAX)
   - Enter flight distance (e.g., 2475 miles)
   - Select month (e.g., July)
   - Select day of week (e.g., Wednesday)
   - Enter departure hour (e.g., 14 for 2 PM)

2. **Click "Predict Delay"**
   - System fetches weather data
   - Combines with flight information
   - Runs ML model prediction

3. **View Results**
   - Delay probability percentage
   - Status (On Time / Likely Delayed)
   - Current weather conditions
   - Weather severity index

### Viewing Analytics

1. Click "Analytics" in navigation
2. View statistics:
   - Total flights analyzed
   - Number of delayed flights
   - Overall delay rate
3. Click "Generate Charts" to see:
   - Delay distribution histogram
   - Average delays by airline
   - Seasonal delay patterns

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Dataset not found"

**Solution:**
```bash
# Check if file exists
dir data\flights.csv

# If not, generate sample data
python generate_sample_data.py
```

### Issue: "Model not loaded"

**Solution:**
```bash
# Train the model
cd src
python train_model.py
cd ..
```

### Issue: Weather API returns errors

**Possible Causes:**
1. Invalid API key
2. No internet connection
3. Rate limit exceeded (60 calls/minute)

**Solution:**
```bash
# Verify API key is set
echo %OPENWEATHER_API_KEY%

# Test API manually
python -c "from src.weather_api import WeatherAPI; api = WeatherAPI(); print(api.get_weather('New York'))"
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# Use different port
# Edit app.py, change last line to:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Charts not displaying

**Solution:**
1. Ensure dataset is loaded
2. Click "Generate Charts" button
3. Check browser console for errors
4. Verify matplotlib is installed: `pip install matplotlib`

---

## Advanced Configuration

### Changing Delay Threshold

Default: 15 minutes

To change:
1. Open `src/data_preprocessing.py`
2. Find `create_target()` method
3. Modify `delay_threshold` parameter
4. Retrain model

### Adding More Airports

1. Open `templates/index.html`
2. Add options to airport dropdowns
3. Open `src/weather_api.py`
4. Add airport-city mapping to `AIRPORT_CITY_MAP`

### Customizing UI

1. Edit `static/css/style.css` for styling
2. Edit `templates/index.html` for structure
3. Edit `static/js/script.js` for functionality

---

## Production Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.9.0" > runtime.txt

# Deploy
heroku create your-app-name
git push heroku main
heroku config:set OPENWEATHER_API_KEY=your_key
```

### AWS Deployment

1. Create EC2 instance
2. Install Python and dependencies
3. Clone repository
4. Set up Nginx reverse proxy
5. Use Gunicorn as WSGI server
6. Configure security groups

### Docker Deployment

```bash
# Build image
docker build -t flight-delay-app .

# Run container
docker run -p 5000:5000 -e OPENWEATHER_API_KEY=your_key flight-delay-app
```

---

## Maintenance

### Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Retraining Model

```bash
# With new data
cd src
python train_model.py
cd ..
```

### Backing Up

Important files to backup:
- `models/` folder (trained models)
- `data/flights.csv` (dataset)
- `src/` folder (custom code)

---

## Getting Help

### Resources

- **README.md** - Project overview
- **DOCUMENTATION.md** - Technical details
- **test_system.py** - System diagnostics

### Common Commands

```bash
# Activate environment
venv\Scripts\activate

# Run tests
python test_system.py

# Start app
python app.py

# Generate sample data
python generate_sample_data.py

# Train model
cd src && python train_model.py
```

---

## Next Steps

After successful setup:

1. ✅ Test with different flight combinations
2. ✅ Explore analytics dashboard
3. ✅ Try different times of day
4. ✅ Compare different airlines
5. ✅ Experiment with weather conditions

**Enjoy predicting flight delays!** ✈️

---

**Need Help?** Check DOCUMENTATION.md for technical details.
