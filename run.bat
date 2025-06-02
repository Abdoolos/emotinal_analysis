@echo off
setlocal enabledelayedexpansion

echo ╭──────────────────────────────────────────╮
echo │    نظام تحليل المشاعر - Emotion Detection    │
echo │    المصمم: عبدالله العويس                   │
echo ╰──────────────────────────────────────────╯

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version > nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate
if errorlevel 1 (
    echo Error activating virtual environment
    pause
    exit /b 1
)

REM Set project root directory
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"

REM Install backend dependencies
echo Installing backend dependencies...
if not exist "%BACKEND_DIR%\requirements.txt" (
    echo Error: requirements.txt not found in %BACKEND_DIR%
    pause
    exit /b 1
)

REM Update pip first
echo Updating pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Error updating pip
    pause
    exit /b 1
)

REM Update setuptools and wheel
echo Installing core packages...
python -m pip install --upgrade setuptools wheel
if errorlevel 1 (
    echo Error installing core packages
    pause
    exit /b 1
)

REM Install PyTorch first
echo Installing PyTorch...
python -m pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo Error installing PyTorch
    pause
    exit /b 1
)

REM Install transformers and its dependencies
echo Installing transformers and dependencies...
python -m pip install --no-cache-dir tokenizers==0.21.1
if errorlevel 1 (
    echo Error installing tokenizers
    pause
    exit /b 1
)

python -m pip install --no-cache-dir transformers
if errorlevel 1 (
    echo Error installing transformers
    pause
    exit /b 1
)

python -m pip install fastapi==0.100.0 uvicorn==0.22.0 python-multipart==0.0.6
if errorlevel 1 (
    echo Error installing FastAPI and dependencies
    pause
    exit /b 1
)

REM Install scientific packages one by one
echo Installing scientific packages...
python -m pip install --no-cache-dir numpy
if errorlevel 1 (
    echo Error installing numpy
    pause
    exit /b 1
)

python -m pip install --no-cache-dir scikit-learn
if errorlevel 1 (
    echo Error installing scikit-learn
    pause
    exit /b 1
)

python -m pip install --no-cache-dir soundfile
if errorlevel 1 (
    echo Error installing soundfile
    pause
    exit /b 1
)

python -m pip install --no-cache-dir numba
if errorlevel 1 (
    echo Error installing numba
    pause
    exit /b 1
)

python -m pip install --no-cache-dir librosa
if errorlevel 1 (
    echo Error installing librosa
    pause
    exit /b 1
)

python -m pip install SpeechRecognition==3.10.0 pydub==0.25.1
if errorlevel 1 (
    echo Error installing audio processing packages
    pause
    exit /b 1
)

REM Install frontend dependencies
echo Installing frontend dependencies...
if exist "%FRONTEND_DIR%\package.json" (
    cd "%FRONTEND_DIR%"
    call npm install
    if errorlevel 1 (
        echo Error installing frontend dependencies
        cd "%PROJECT_ROOT%"
        pause
        exit /b 1
    )
    cd "%PROJECT_ROOT%"
) else (
    echo Error: package.json not found in %FRONTEND_DIR%
    pause
    exit /b 1
)

REM Run the application
echo Starting the application...
python start.py

REM Deactivate virtual environment
call venv\Scripts\deactivate

pause
