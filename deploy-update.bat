@echo off
echo Updating repository...
cd %~dp0

echo Committing changes...
git add .
git commit -m "Update deployment configuration"
git push

echo Done! Now you can deploy:
echo Backend: https://dashboard.render.com/new
echo Frontend: https://vercel.com/new
echo.
echo Steps for Render (Backend):
echo 1. Click New Web Service
echo 2. Connect your GitHub repository
echo 3. Select the repository
echo 4. Use these settings:
echo    - Name: emotion-detection-api
echo    - Runtime: Python
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: cd backend/src ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo.
echo Steps for Vercel (Frontend):
echo 1. Import your GitHub repository
echo 2. Configure the project:
echo    - Framework: Create React App
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo    - Output Directory: build
echo.
pause
