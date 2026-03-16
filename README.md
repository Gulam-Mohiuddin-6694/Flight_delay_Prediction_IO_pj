# Flight Delay Prediction Web Application

A full-stack machine learning web application that predicts flight delays using historical flight data and real-time weather information.

## Features

- **Machine Learning Models**: Logistic Regression, Random Forest, and Gradient Boosting
- **Real-time Weather Integration**: OpenWeather API for current weather conditions
- **Interactive Web Interface**: Clean, modern, and responsive UI
- **Analytics Dashboard**: Visualizations and insights from historical data
- **Comprehensive Predictions**: Delay probability with weather impact analysis

## Technology Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- pandas & numpy (Data Processing)
- matplotlib & seaborn (Visualization)

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)

## Project Structure

```
flight-delay-webapp/
│
├── data/
│   └── flights.csv              # Flight dataset (download from Kaggle)
│
├── models/
│   ├── delay_model.pkl          # Trained ML model
│   ├── preprocessor.pkl         # Data preprocessor
│   └── feature_columns.pkl      # Feature column names
│
├── static/
│   ├── css/
│   │   └── style.css           # Stylesheet
│   └── js/
│       └── script.js           # Frontend JavaScript
│
├── templates/
│   ├── index.html              # Home page
│   └── analytics.html          # Analytics dashboard
│
├── src/
│   ├── data_preprocessing.py   # Data preprocessing module
│   ├── train_model.py          # Model training script
│   ├── weather_api.py          # Weather API integration
│   └── predict.py              # Prediction module
│
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Installation

### 1. Clone or Download the Project

```bash
cd flight-delay-webapp
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Dataset

Download a flight delay dataset from Kaggle:
- **Recommended**: [Flight Delays and Cancellations](https://www.kaggle.com/datasets/usdot/flight-delays)
- Alternative: [Airline On-Time Performance](https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018)

Place the CSV file in the `data/` folder and rename it to `flights.csv`.

### 5. Get OpenWeather API Key

1. Sign up at [OpenWeather](https://openweathermap.org/api)
2. Get your free API key
3. Set environment variable:

```bash
# Windows
set OPENWEATHER_API_KEY=your_api_key_here

# Linux/Mac
export OPENWEATHER_API_KEY=your_api_key_here
```

Or edit `src/weather_api.py` and replace `YOUR_API_KEY_HERE` with your actual API key.

## Usage

### 1. Train the Model

```bash
cd src
python train_model.py
```

This will:
- Load and preprocess the dataset
- Train multiple ML models
- Select the best performing model
- Save the trained model and preprocessor

### 2. Run the Web Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### 3. Make Predictions

1. Open your browser and go to `http://localhost:5000`
2. Fill in the flight details form:
   - Airline
   - Origin Airport
   - Destination Airport
   - Flight Distance
   - Departure Time
   - Day of Week
   - Month
3. Click "Predict Delay"
4. View the prediction result with weather information

### 4. View Analytics

Navigate to the Analytics page to see:
- Total flights and delay statistics
- Delay distribution charts
- Delays by airline
- Delays by month
- Weather impact analysis

## Dataset Requirements

Your dataset should include these columns (or similar):
- `OP_CARRIER` or `AIRLINE`: Airline code
- `ORIGIN`: Origin airport code
- `DEST`: Destination airport code
- `DISTANCE`: Flight distance in miles
- `MONTH`: Month of flight
- `DAY_OF_WEEK`: Day of week (1-7)
- `CRS_DEP_TIME`: Scheduled departure time
- `DEP_DELAY` or `DEPARTURE_DELAY`: Departure delay in minutes

## API Endpoints

- `GET /`: Home page with prediction form
- `POST /predict`: Make flight delay prediction
- `GET /analytics`: Analytics dashboard
- `GET /api/analytics-data`: Get analytics statistics
- `GET /generate-charts`: Generate visualization charts

## Model Performance

The system trains and compares three models:
1. **Logistic Regression**: Fast, interpretable baseline
2. **Random Forest**: Ensemble method with good accuracy
3. **Gradient Boosting**: Advanced ensemble with best performance

The best model is automatically selected based on F1 score.

## Weather Features

The system extracts these weather features:
- Temperature (°C)
- Humidity (%)
- Wind Speed (m/s)
- Visibility (meters)
- Pressure (hPa)
- Weather Severity Index (0-10)

## Customization

### Adding More Airlines/Airports

Edit `templates/index.html` and add options to the select dropdowns.

### Adjusting Delay Threshold

Edit `src/data_preprocessing.py` and modify the `delay_threshold` parameter in the `create_target()` method.

### Changing Model Parameters

Edit `src/train_model.py` and adjust the model hyperparameters.

## Troubleshooting

### Model Not Loading
- Ensure you've run `train_model.py` first
- Check that `models/` directory contains the .pkl files

### Weather API Errors
- Verify your API key is correct
- Check your internet connection
- Ensure you haven't exceeded API rate limits (60 calls/minute for free tier)

### Dataset Errors
- Verify the CSV file is in `data/flights.csv`
- Check that required columns exist in your dataset
- Ensure there's enough data (at least 10,000 rows recommended)

## Future Enhancements

- Add more ML models (XGBoost, LightGBM)
- Implement feature importance visualization
- Add historical delay statistics by route
- Include airport congestion data
- Add user authentication
- Deploy to cloud platform (AWS, Heroku, etc.)

## License

This project is for educational purposes.

## Credits

- Flight data: Kaggle
- Weather data: OpenWeather API
- ML libraries: scikit-learn
- Web framework: Flask

## Contact

For questions or issues, please open an issue in the repository.
