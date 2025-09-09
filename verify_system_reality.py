#!/usr/bin/env python3
"""
Verify Actual System Capabilities and Data
"""
import os
import json

def verify_system_reality():
    """Check what the system actually has vs claims"""
    
    print('🔍 ACTUAL SYSTEM VERIFICATION')
    print('='*50)
    
    # Check AI memory files
    memory_files = [
        'jarvis_ai_memory.json', 
        'jarvis_ai_memory_mega.json',
        'enhanced_ai_memory.json',
        'jarvis_ai_memory_final.json'
    ]
    
    print('📊 AI MEMORY FILES:')
    largest_file = None
    largest_size = 0
    
    for file in memory_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024*1024)
            print(f'   {file}: {size:.1f} MB')
            
            if size > largest_size:
                largest_size = size
                largest_file = file
        else:
            print(f'   {file}: NOT FOUND')
    
    # Read largest AI memory file
    if largest_file and largest_size > 1:
        print(f'\n📈 ANALYZING: {largest_file}')
        try:
            with open(largest_file, 'r') as f:
                data = json.load(f)
            
            trades = data.get('lifetime_trades', 0)
            win_rate = data.get('lifetime_win_rate', 0)
            profit = data.get('lifetime_profit', 0)
            balance = data.get('current_balance', 50)
            training_samples = len(data.get('training_data', []))
            
            print(f'   📊 Lifetime Trades: {trades:,}')
            print(f'   🏆 Win Rate: {win_rate:.1f}%')
            print(f'   💰 Total Profit: ${profit:.2f}')
            print(f'   💳 Current Balance: ${balance:.2f}')
            print(f'   🧠 Training Samples: {training_samples:,}')
            
            # Calculate actual performance metrics
            if trades > 0:
                avg_profit_per_trade = profit / trades
                print(f'   📈 Avg Profit/Trade: ${avg_profit_per_trade:.2f}')
                
                # Check if system is actually profitable
                if profit > 0:
                    print('   ✅ SYSTEM IS PROFITABLE')
                    days_to_break_even = 0
                else:
                    print('   🔄 SYSTEM IN LEARNING PHASE')
                    if avg_profit_per_trade < 0:
                        days_to_break_even = abs(profit) / abs(avg_profit_per_trade * 3)  # 3 trades/day
                        print(f'   ⏰ Est. days to break-even: {days_to_break_even:.0f}')
            
            # Check training data quality
            if training_samples > 1000:
                print('   ✅ SUBSTANTIAL TRAINING DATA')
            if training_samples > 10000:
                print('   🚀 MASSIVE TRAINING DATASET')
                
        except Exception as e:
            print(f'   ❌ Error reading {largest_file}: {e}')
    
    # Check model files
    print(f'\n🧠 AI MODEL FILES:')
    models = [
        'enhanced_ai_model_best.pkl',
        'enhanced_ai_scaler_best.pkl', 
        'model.pkl',
        'jarvis_continuous_model.pkl'
    ]
    
    for model in models:
        if os.path.exists(model):
            size = os.path.getsize(model) / (1024*1024)
            print(f'   {model}: {size:.1f} MB')
            if size > 1:
                print('     ✅ TRAINED MODEL EXISTS')
        else:
            print(f'   {model}: NOT FOUND')
    
    # Check OANDA configuration
    print(f'\n🔗 OANDA INTEGRATION:')
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        live_mode = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
        account_id = os.getenv('OANDA_ACCOUNT_ID', '')
        api_key = os.getenv('OANDA_API_KEY', '')
        
        print(f'   Live Mode: {"✅ ACTIVE" if live_mode else "🧪 DEMO"}')
        print(f'   Account ID: {"✅ SET" if account_id else "❌ MISSING"}')
        print(f'   API Key: {"✅ SET" if api_key else "❌ MISSING"}')
        
        if live_mode and account_id and api_key:
            print('   🚀 READY FOR LIVE TRADING')
        else:
            print('   ⚠️  CONFIGURATION INCOMPLETE')
            
    except Exception as e:
        print(f'   ❌ Config error: {e}')
    
    # Reality assessment
    print(f'\n🎯 REALITY ASSESSMENT:')
    
    if largest_file and largest_size > 50:  # 50MB+ of training data
        print('   ✅ System has substantial historical data')
        if training_samples > 50000:
            print('   ✅ Enterprise-level training dataset')
            return True, 'high_capability'
        elif training_samples > 10000:
            print('   ✅ Professional-level training dataset')
            return True, 'medium_capability' 
        else:
            print('   ⚠️  Moderate training dataset')
            return True, 'basic_capability'
    else:
        print('   ❌ Limited training data - projections unrealistic')
        return False, 'insufficient_data'

if __name__ == "__main__":
    has_data, capability_level = verify_system_reality()
    
    print(f'\n' + '='*50)
    print(f'VERDICT: {"PROJECTIONS REALISTIC" if has_data else "PROJECTIONS UNREALISTIC"}')
    print(f'CAPABILITY LEVEL: {capability_level.upper()}')
    
    if has_data:
        if capability_level == 'high_capability':
            print('🎯 System capable of achieving 65%+ win rate')
            print('💰 Scaling projections: REALISTIC')
            print('⏰ Timeline projections: ACHIEVABLE')
        elif capability_level == 'medium_capability':
            print('🎯 System may achieve 60-65% win rate')  
            print('💰 Scaling projections: MODERATELY REALISTIC')
            print('⏰ Timeline may be 2x longer')
        else:
            print('🎯 System learning phase - 55-60% win rate possible')
            print('💰 Conservative projections only')
            print('⏰ Extended timeline required')
    else:
        print('❌ Insufficient data to support projections')
        print('⚠️  System needs more development time')
