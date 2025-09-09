#!/usr/bin/env python3
"""
Simple Flask Starter with Enhanced Logging
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Starting Flask Webhook Server...")
print("Webhook URL: http://localhost:5000/webhook")
print("Dashboard URL: http://localhost:5000")
print("Memory logging: ENABLED")
print("Auto-sync: ENABLED")
print("-" * 50)

# Import and start the Flask app
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
