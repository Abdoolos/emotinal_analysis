@echo off
echo Updating repository...
cd %~dp0

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Update deployment configuration with requirements.txt"

echo Pushing to GitHub...
git push

if errorlevel 1 (
    echo Error occurred while pushing to GitHub
    pause
    exit /b 1
)

echo.
echo Successfully updated repository!
echo.
echo Next steps for deployment:
echo.
echo 1. Backend (Render):
echo    Open: https://dashboard.render.com/new
echo    - Click "New Web Service"
echo    - Connect GitHub repository
echo    - Name: emotion-detection-api
echo    - Root Directory: ./
echo    - Runtime: Python
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: cd backend/src ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo.
echo 2. Frontend (Vercel):
echo    Open: https://vercel.com/new
echo    - Import your GitHub repository
echo    - Root Directory: frontend
echo    - Framework: Create React App
echo    - Environment Variables:
echo      REACT_APP_API_URL=https://[your-render-service-name].onrender.com
echo.
echo After deployment:
echo 1. Copy your Render backend URL
echo 2. Add it to Vercel frontend environment variables
echo 3. Redeploy the frontend
echo.
pause
