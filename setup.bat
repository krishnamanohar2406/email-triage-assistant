@echo off
REM Email Triage Assistant - Windows Setup Script

echo ==========================================
echo EMAIL TRIAGE ASSISTANT - SETUP
echo ==========================================
echo.

REM Check if .env exists
if exist .env (
    echo [OK] .env file found
) else (
    echo [!] .env file not found. Creating...
    (
        echo SCALEDOWN_API_KEY=your_scaledown_api_key_here
        echo GEMINI_API_KEY=your_gemini_api_key_here
    ) > .env
    echo [OK] .env file created
)

echo.
echo ==========================================
echo NEXT STEPS:
echo ==========================================
echo.
echo 1. Open .env file in Notepad
echo 2. Replace the placeholder text with your real API keys
echo 3. Save the file
echo 4. Run: python email_triage_assistant.py
echo.
echo Opening .env file now...
echo.

REM Open .env in notepad
notepad .env

echo.
echo After saving your API keys, press any key to test...
pause >nul

echo.
echo Testing configuration...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); scaledown=os.getenv('SCALEDOWN_API_KEY'); gemini=os.getenv('GEMINI_API_KEY'); print('ScaleDown:', 'CONFIGURED' if scaledown and scaledown != 'your_scaledown_api_key_here' else 'NOT CONFIGURED'); print('Gemini:', 'CONFIGURED' if gemini and gemini != 'your_gemini_api_key_here' else 'NOT CONFIGURED')"

echo.
echo Setup complete! Run: python email_triage_assistant.py
pause
