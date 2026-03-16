# Flight Delay Prediction - Technical Documentation

## Project Overview

This is a full-stack machine learning web application that predicts flight delays by combining historical flight data with real-time weather information.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (HTML/CSS/JavaScript)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask Web Server                         │
│                        (app.py)                              │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                       │
         ▼                                       ▼
┌──────────────────────┐              ┌──────────────────────┐
│  Prediction Module   │              │  Analytics Module    │
│   (predict.py)       │              │   (app.py)           │
└──────┬───────────────┘              └──────────────────────┘
       │
       ├─────────────┬──────────────┬──────────────┐
       ▼             ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   ML     │  │  Data    │  │ Weather  │  │  Saved   │
│  Model   │  │  Prep    │  │   API    │  │  Models  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Module Descriptions

### 1. Data Preprocessing (data_preprocessing.py)

**Purpose**: Clean, transform, and prepare flight data for machine learning

**Key Functions**:
- `load_data()`: Load CSV dataset
- `clean_data()`: Remove missing values and outliers
- `create_features()`: Engineer new features (peak hours, weekends)
- `encode_categorical()`: Convert categorical variables to numerical
- `create_target()`: Generate binary delay classification
- `prepare_features()`: Scale numerical features

**Feature Engineering**:
- Peak Hour Detection: Identifies rush hours (6-9 AM, 4-7 PM)
- Weekend Flag: Binary indicator for Saturday/Sunday
- Time-based Features: Hour extraction from departure time

### 2. Model Training (train_model.py)

**Purpose**: Train and evaluate multiple ML models, select the best performer

**Models Trained**:
1. Logistic Regression - Fast baseline model
2. Random Forest - Ensemble method with feature importance
3. Gradient Boosting - Advanced ensemble technique

**Evaluation Metrics**:
- Accuracy: Overall correctness
- Precision: Correct positive predictions
- Recall: Coverage of actual positives
- F1 Score: Harmonic mean of precision and recall
- Confusion Matrix: Detailed classification breakdown

**Model Selection**: Automatically selects model with highest F1 score

### 3. Weather API Integration (weather_api.py)

**Purpose**: Fetch and process real-time weather data

**Features**:
- OpenWeather API integration
- Airport-to-city mapping
- Weather severity calculation
- Graceful error handling with fallback values

**Weather Features Extracted**:
- Temperature (°C)
- Humidity (%)
- Wind Speed (m/s)
- Visibility (meters)
- Atmospheric Pressure (hPa)
- Weather Severity Index (0-10)

**Severity Calculation**:
```
Base Score = 0
+ Severe weather (thunderstorm, snow): +5
+ Rain/drizzle: +3
+ Fog/mist: +2
+ High wind (>15 m/s): +3
+ Low visibility (<1km): +2
Maximum: 10
```

### 4. Prediction Module (predict.py)

**Purpose**: Make real-time delay predictions

**Process Flow**:
1. Load trained model and preprocessor
2. Fetch weather data for origin airport
3. Combine flight data with weather features
4. Encode and scale input features
5. Generate prediction with probability
6. Return structured result

**Output Format**:
```json
{
    "prediction": 0 or 1,
    "probability": 0-100,
    "status": "On Time" or "Likely Delayed",
    "weather": {...}
}
```

### 5. Flask Application (app.py)

**Purpose**: Web server and API endpoints

**Routes**:
- `GET /`: Home page with prediction form
- `POST /predict`: Process prediction request
- `GET /analytics`: Analytics dashboard
- `GET /api/analytics-data`: Dataset statistics
- `GET /generate-charts`: Create visualization charts

**Error Handling**:
- Model loading failures
- Invalid input validation
- API timeout handling
- Dataset access errors

## Data Flow

### Prediction Request Flow

```
User Input → Form Submission → Flask Route
                                    ↓
                            Validate Input
                                    ↓
                            Fetch Weather Data
                                    ↓
                            Combine Features
                                    ↓
                            Encode & Scale
                                    ↓
                            ML Model Prediction
                                    ↓
                            Format Response
                                    ↓
                            Return JSON
                                    ↓
                            Display Result
```

## Machine Learning Pipeline

### Training Pipeline

```
Raw Data → Clean → Feature Engineering → Encoding → Scaling
                                                        ↓
                                                   Split Data
                                                        ↓
                                            Train Multiple Models
                                                        ↓
                                                Evaluate & Compare
                                                        ↓
                                                Select Best Model
                                                        ↓
                                                Save Model & Preprocessor
```

### Prediction Pipeline

```
User Input → Fetch Weather → Combine Features → Load Preprocessor
                                                        ↓
                                                Encode Categories
                                                        ↓
                                                Scale Features
                                                        ↓
                                                Load Model
                                                        ↓
                                                Predict
                                                        ↓
                                                Return Probability
```

## Database Schema (CSV Format)

### Required Columns

| Column | Type | Description |
|--------|------|-------------|
| OP_CARRIER | String | Airline code (AA, DL, UA, etc.) |
| ORIGIN | String | Origin airport code |
| DEST | String | Destination airport code |
| DISTANCE | Integer | Flight distance in miles |
| MONTH | Integer | Month (1-12) |
| DAY_OF_WEEK | Integer | Day of week (1-7) |
| CRS_DEP_TIME | Integer | Scheduled departure time (HHMM) |
| DEP_DELAY | Float | Departure delay in minutes |

## API Integration

### OpenWeather API

**Endpoint**: `https://api.openweathermap.org/data/2.5/weather`

**Parameters**:
- `q`: City name
- `appid`: API key
- `units`: metric (for Celsius)

**Rate Limits** (Free Tier):
- 60 calls/minute
- 1,000,000 calls/month

**Response Structure**:
```json
{
    "main": {
        "temp": 20.5,
        "humidity": 65,
        "pressure": 1013
    },
    "wind": {
        "speed": 5.2
    },
    "visibility": 10000,
    "weather": [
        {"main": "Clear"}
    ]
}
```

## Frontend Architecture

### HTML Structure

- **index.html**: Main prediction interface
  - Form with flight details
  - Loading animation
  - Result display section

- **analytics.html**: Data visualization dashboard
  - Statistics cards
  - Chart generation
  - Historical insights

### CSS Design

- **Responsive Grid Layout**: Adapts to screen sizes
- **Gradient Background**: Modern purple gradient
- **Card-based UI**: Clean, organized sections
- **Smooth Animations**: Loading spinners, hover effects

### JavaScript Functionality

- **Form Handling**: Async submission with fetch API
- **Loading States**: Show/hide loading animation
- **Dynamic Content**: Update results without page reload
- **Error Handling**: User-friendly error messages

## Performance Considerations

### Optimization Strategies

1. **Model Loading**: Load once at startup, reuse for predictions
2. **Data Sampling**: Limit analytics to 10,000 records for speed
3. **Caching**: Browser caches static assets
4. **Async Operations**: Non-blocking API calls

### Scalability

**Current Limitations**:
- Single-threaded Flask development server
- In-memory model storage
- Synchronous weather API calls

**Production Improvements**:
- Use Gunicorn/uWSGI for multi-threading
- Implement Redis caching for weather data
- Add database for prediction history
- Deploy on cloud platform (AWS, Heroku)

## Security Considerations

### Current Implementation

- API key stored in environment variable
- Input validation on form submission
- Error messages don't expose system details

### Production Recommendations

- Use HTTPS for all communications
- Implement rate limiting
- Add user authentication
- Sanitize all user inputs
- Use secrets management service (AWS Secrets Manager)
- Enable CORS properly
- Add CSRF protection

## Testing Strategy

### Unit Tests (Recommended)

```python
# Test data preprocessing
test_load_data()
test_clean_data()
test_feature_engineering()

# Test model
test_model_training()
test_model_prediction()

# Test weather API
test_weather_fetch()
test_weather_feature_extraction()

# Test Flask routes
test_home_route()
test_predict_route()
test_analytics_route()
```

### Integration Tests

- End-to-end prediction flow
- Weather API integration
- Model loading and prediction
- Chart generation

## Deployment Guide

### Local Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Generate/download dataset
3. Train model: `python src/train_model.py`
4. Set API key: `set OPENWEATHER_API_KEY=your_key`
5. Run app: `python app.py`

### Cloud Deployment (Heroku Example)

```bash
# Create Procfile
web: gunicorn app:app

# Create runtime.txt
python-3.9.0

# Deploy
heroku create flight-delay-predictor
git push heroku main
heroku config:set OPENWEATHER_API_KEY=your_key
```

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Troubleshooting

### Common Issues

**Issue**: Model not loading
- **Solution**: Run `train_model.py` first

**Issue**: Weather API errors
- **Solution**: Check API key, verify internet connection

**Issue**: Dataset errors
- **Solution**: Verify CSV format, check column names

**Issue**: Import errors
- **Solution**: Activate virtual environment, reinstall dependencies

## Future Enhancements

### Short-term
- Add more airlines and airports
- Implement feature importance visualization
- Add historical delay trends
- Include airport congestion data

### Long-term
- Real-time flight tracking integration
- Mobile application
- Email/SMS notifications
- Multi-language support
- Advanced models (Neural Networks)
- A/B testing framework

## Performance Metrics

### Expected Model Performance

- **Accuracy**: 75-85%
- **Precision**: 70-80%
- **Recall**: 65-75%
- **F1 Score**: 70-78%

### Response Times

- **Prediction**: 1-3 seconds (including weather API)
- **Analytics**: 2-5 seconds (with chart generation)
- **Page Load**: <1 second

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Retrain model quarterly with new data
- Monitor API usage and costs
- Review and update airport/airline lists
- Check for security vulnerabilities

### Monitoring

- Track prediction accuracy
- Monitor API response times
- Log error rates
- Analyze user patterns

## License & Credits

- **Dataset**: Kaggle (various contributors)
- **Weather Data**: OpenWeather API
- **ML Framework**: scikit-learn
- **Web Framework**: Flask

---

**Last Updated**: 2024
**Version**: 1.0.0
**Author**: Flight Delay Prediction Team
