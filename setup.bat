@echo off

REM Check if requirements.txt exists
IF NOT EXIST "requirements.txt" (
    echo "requirements.txt not found. Please ensure the file exists in the current directory."
    exit /b 1
)

REM Set up the virtual environment
echo Creating virtual environment...
python -m venv venv

REM Check if the virtual environment was created successfully
IF NOT EXIST "venv" (
    echo "Failed to create virtual environment."
    exit /b 1
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Check if installation was successful
IF %ERRORLEVEL% NEQ 0 (
    echo "Failed to install dependencies."
    exit /b 1
)

REM Confirm setup completion
echo "Setup complete. Virtual environment is activated and dependencies are installed."
