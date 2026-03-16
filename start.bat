@echo off
echo ============================================================
echo Starting Flight Delay Prediction Application
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if model exists
if not exist "models\delay_model.pkl" (
    echo WARNING: Trained model not found!
    echo Please train the model first by running:
    echo   cd src
    echo   python train_model.py
    echo.
    pause
)

REM Start the application
echo Starting Flask application...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
