@echo off
REM Activate virtual environment
call venv\Scripts\activate

REM Change to the backend directory
cd backend

REM Start Uvicorn server on port 8080 and wait for it to complete
echo Starting Uvicorn on port 8080...
uvicorn app:app --port 8080

REM Cleanup and deactivate virtual environment after Uvicorn stops
echo Stopping server and performing cleanup...
cd ..
call venv\Scripts\deactivate
echo Virtual environment deactivated.
