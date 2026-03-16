@echo off
echo ============================================================
echo Flight API Key Setup Helper
echo ============================================================
echo.

echo Enter your AviationStack API key:
echo (Get it from: https://aviationstack.com/dashboard)
echo.
set /p APIKEY="API Key: "

if "%APIKEY%"=="" (
    echo ERROR: No API key entered
    pause
    exit /b 1
)

echo.
echo Setting API key...
set AVIATIONSTACK_API_KEY=%APIKEY%

echo.
echo Testing API connection...
python test_api_connection.py

echo.
echo ============================================================
echo If test shows "Source: api" then it's working!
echo.
echo To start the app with this API key, run:
echo   python app.py
echo.
echo NOTE: This API key is only set for this command prompt session.
echo To set it permanently, run:
echo   setx AVIATIONSTACK_API_KEY "%APIKEY%"
echo ============================================================
pause
