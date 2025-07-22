#!/bin/bash
# JARVIS Trading System Startup Script

echo "Starting JARVIS AI Trading System..."

# Check if emergency stop flag exists
if [ -f "EMERGENCY_STOP.flag" ]; then
    echo "Emergency stop flag detected! Remove flag file to start."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Run system validation
echo "Running system validation..."
python validate_system.py
if [ $? -ne 0 ]; then
    echo "System validation failed!"
    exit 1
fi

# Start health monitor in background
echo "Starting health monitor..."
python health_monitor.py --continuous 300 &
HEALTH_MONITOR_PID=$!
echo $HEALTH_MONITOR_PID > health_monitor.pid

# Start trading system
echo "Starting trading system..."
python start_trading_bot.py

# Cleanup on exit
kill $HEALTH_MONITOR_PID 2>/dev/null
rm -f health_monitor.pid

echo "JARVIS Trading System stopped"
