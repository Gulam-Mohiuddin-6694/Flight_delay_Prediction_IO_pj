@echo off
echo ============================================================
echo Flight Delay Prediction - Automated Setup
echo ============================================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 4: Generating sample dataset...
python generate_sample_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate sample dataset
    pause
    exit /b 1
)
echo.

echo Step 5: Training model...
cd src
python train_model.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to train model
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run: python app.py
echo 3. Open browser: http://localhost:5000
echo.
echo Note: Set your OpenWeather API key before running:
echo set OPENWEATHER_API_KEY=your_key_here
echo.
pause
