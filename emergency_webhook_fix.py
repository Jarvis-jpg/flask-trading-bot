#!/usr/bin/env python3
"""
Emergency webhook fix deployment script
This will create a simple webhook endpoint that handles both field names
"""

import os
import shutil

def deploy_emergency_fix():
    """Deploy emergency fix for webhook"""
    print("🚨 DEPLOYING EMERGENCY WEBHOOK FIX")
    print("=" * 50)
    
    # Create a simple fixed webhook file
    webhook_fix = '''
def webhook_fixed():
    """Fixed webhook that handles both pair and symbol"""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        try:
            # Handle both 'pair' and 'symbol' field names - THE FIX!
            trading_pair = data.get('pair') or data.get('symbol') or 'EURUSD'
            
            # Log the fix working
            print(f"✅ WEBHOOK FIX WORKING: Using {trading_pair} from data: {data}")
            
            # First check market status with the fixed field
            market_check = analyzer.analyze_trade(trading_pair, None)
            
            if market_check.get('status') == 'market_closed':
                return jsonify({
                    'status': 'rejected',
                    'reason': 'market_closed', 
                    'details': market_check
                }), 200

            # If market is open, analyze the trade setup
            analysis = analyzer.analyze_trade(trading_pair, data)
            
            # Check if analysis recommends the trade
            if analysis.get('prediction', {}).get('recommended', False):
                # Execute trade on OANDA
                trade_result = oanda.place_trade(data)
                
                if trade_result and trade_result.get('success'):
                    log_data = {
                        'timestamp': datetime.now().isoformat(),
                        'signal_data': data,
                        'trade_result': trade_result,
                        'analysis': analysis
                    }
                    log_trade(log_data)
                    
                    # Track trade performance for model improvement
                    analyzer.track_trade_performance({
                        'pair': trading_pair,  # Using the fixed field
                        'profit': trade_result.get('profit', 0),
                        'entry_price': trade_result.get('filled_price'),
                        'exit_price': None,
                        'duration': 0,
                        'confidence': data.get('confidence', 0)
                    })
                    
                    return jsonify({
                        'status': 'success',
                        'message': 'Trade executed successfully',
                        'trade_id': trade_result.get('trade_id'),
                        'analysis': analysis
                    }), 200
                else:
                    return jsonify({
                        'status': 'failed',
                        'message': 'Trade execution failed',
                        'analysis': analysis
                    }), 200
            else:
                return jsonify({
                    'status': 'rejected',
                    'reason': 'analysis_failed',
                    'message': 'Analysis does not recommend this trade',
                    'analysis': analysis
                }), 200
                
        except Exception as e:
            print(f"❌ Error in webhook: {e}")
            import traceback
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
'''
    
    print("✅ Emergency webhook fix prepared!")
    print("🔧 This fix handles both 'pair' and 'symbol' field names")
    print("\n📋 MANUAL DEPLOYMENT OPTIONS:")
    print("1. Wait for Render auto-deployment (may take time)")
    print("2. Trigger manual deployment in Render dashboard")
    print("3. Create new deployment branch")
    
    return webhook_fix

if __name__ == "__main__":
    deploy_emergency_fix()
