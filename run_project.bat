@echo off
echo ================================
echo    Starting Ilaaj Buddy... 💊
echo ================================

REM Start Backend
echo Starting Backend...
start cmd /k "cd /d C:\Users\HP\Documents\healthcare-chatbot\backend\app && ..\venv\Scripts\activate && uvicorn main:app --reload"

REM Wait 5 seconds for backend to start
timeout /t 5

REM Start Frontend
echo Starting Frontend...
start cmd /k "cd /d C:\Users\HP\Documents\healthcare-chatbot\frontend && npm start"

echo ================================
echo   Ilaaj Buddy is running! 💊
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo ================================
pause