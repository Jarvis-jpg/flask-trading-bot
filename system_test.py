#!/usr/bin/env python3
"""
System Test Script for Flask Trading Bot
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    results = {}
    
    modules_to_test = [
        ('flask', 'Flask'),
        ('pandas', 'pandas as pd'),
        ('numpy', 'numpy as np'),
        ('sklearn', 'scikit-learn'),
        ('oandapyV20', 'OANDA API'),
        ('dotenv', 'python-dotenv'),
        ('joblib', 'joblib'),
        ('requests', 'requests'),
    ]
    
    for module, name in modules_to_test:
        try:
            __import__(module)
            results[name] = "✓ PASS"
        except ImportError as e:
            results[name] = f"✗ FAIL: {e}"
    
    return results

def test_environment():
    """Test environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = [
        'OANDA_API_KEY',
        'OANDA_ACCOUNT_ID',
        'OANDA_API_URL',
        'OANDA_LIVE'
    ]
    
    results = {}
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive data
            if 'KEY' in var:
                display_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
            else:
                display_value = value
            results[var] = f"✓ SET: {display_value}"
        else:
            results[var] = "✗ NOT SET"
    
    return results

def test_oanda_connection():
    """Test OANDA API connection"""
    try:
        from oanda_client import OandaClient
        client = OandaClient()
        
        # Test getting price data
        price_data = client.get_current_price('EUR_USD')
        
        return {
            'connection': '✓ PASS',
            'price_data': f"✓ PASS: EUR_USD = {price_data.get('bid', 'N/A')}/{price_data.get('ask', 'N/A')}"
        }
    except Exception as e:
        return {
            'connection': f'✗ FAIL: {str(e)[:100]}...',
            'price_data': '✗ SKIP: Connection failed'
        }

def test_trade_analyzer():
    """Test trade analyzer functionality"""
    try:
        from trade_analyzer import TradeAnalyzer
        analyzer = TradeAnalyzer()
        
        # Test basic analysis
        test_data = {
            'pair': 'EUR_USD',
            'action': 'buy',
            'entry': 1.0950,
            'stop_loss': 1.0900,
            'take_profit': 1.1000,
            'units': 1000,
            'confidence': 0.8
        }
        
        analysis = analyzer.analyze_trade('EUR_USD', test_data)
        
        return {
            'analyzer': '✓ PASS',
            'analysis': f"✓ PASS: Status = {analysis.get('status', 'unknown')}"
        }
    except Exception as e:
        return {
            'analyzer': f'✗ FAIL: {str(e)[:100]}...',
            'analysis': '✗ SKIP: Analyzer failed'
        }

def main():
    """Run all system tests"""
    print("🚀 Flask Trading Bot System Test")
    print("=" * 50)
    
    print(f"\n📍 Python Version: {sys.version}")
    print(f"📍 Working Directory: {os.getcwd()}")
    
    # Test imports
    print("\n📦 Testing Module Imports:")
    import_results = test_imports()
    for module, result in import_results.items():
        print(f"  {module:20} {result}")
    
    # Test environment
    print("\n🔧 Testing Environment Variables:")
    env_results = test_environment()
    for var, result in env_results.items():
        print(f"  {var:20} {result}")
    
    # Test OANDA connection
    print("\n🌐 Testing OANDA Connection:")
    oanda_results = test_oanda_connection()
    for test, result in oanda_results.items():
        print(f"  {test:20} {result}")
    
    # Test trade analyzer
    print("\n🧠 Testing Trade Analyzer:")
    analyzer_results = test_trade_analyzer()
    for test, result in analyzer_results.items():
        print(f"  {test:20} {result}")
    
    # Summary
    print("\n📊 Test Summary:")
    all_results = {**import_results, **env_results, **oanda_results, **analyzer_results}
    passed = sum(1 for result in all_results.values() if '✓' in result)
    total = len(all_results)
    
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for trading.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
