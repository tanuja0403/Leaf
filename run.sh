#!/bin/bash

# Leaf Recognition System Startup Script

echo "🚀 Starting Leaf Recognition System..."

# Check if Python and Node.js are installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Initialize node path directly
export PATH="$HOME/.nvm/versions/node/v25.9.0/bin:$PATH"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Start backend in background
echo "📡 Starting Flask backend..."
cd backend
source venv/bin/activate && python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🌐 Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Services started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait