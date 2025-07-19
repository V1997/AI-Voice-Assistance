@echo off
echo 🚀 Setting up AI Voice Assistance Chatbot...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Node.js version: 
node --version

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd ..\backend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed

REM Create .env file for backend
echo 🔧 Creating backend environment file...
(
echo PORT=3001
echo NODE_ENV=development
) > .env
echo ✅ Backend environment file created

cd ..

echo.
echo 🎉 Setup complete! To start the application:
echo.
echo 1. Start the backend server:
echo    cd backend ^&^& npm run dev
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend ^&^& npm run dev
echo.
echo 3. Open your browser to http://localhost:3000
echo.
echo Happy coding! 🚀
pause 