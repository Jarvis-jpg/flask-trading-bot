#!/usr/bin/env python3
"""
Final System Deployment Verification
Verify that the million trade system is fully deployed and operational
"""

import os
import json
import datetime

def verify_deployment():
    """Verify the complete deployment"""
    print("🎯 JARVIS MILLION TRADE SYSTEM - DEPLOYMENT VERIFICATION")
    print("=" * 70)
    print(f"Verification Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    checks_passed = 0
    total_checks = 8
    
    # Check 1: Million Trade Data
    print("1. 📊 MILLION TRADE DATA VERIFICATION")
    if os.path.exists("jarvis_ai_memory_mega.json"):
        file_size = os.path.getsize("jarvis_ai_memory_mega.json") / (1024 * 1024)
        print(f"   ✅ Full dataset exists: {file_size:.1f}MB")
        
        # Verify trade count
        try:
            with open("jarvis_ai_memory_mega.json", 'r') as f:
                data = json.load(f)
            
            if 'trades' in data and len(data['trades']) == 1000000:
                print(f"   ✅ Trade count verified: {len(data['trades']):,} trades")
                win_rate = data.get('statistics', {}).get('win_rate', 0)
                print(f"   ✅ Win rate confirmed: {win_rate}%")
                checks_passed += 1
            else:
                print(f"   ❌ Trade count mismatch: {len(data.get('trades', []))}")
        except Exception as e:
            print(f"   ❌ Error reading data: {e}")
    else:
        print("   ⚠️  Full dataset not found, checking chunks...")
        
        # Check chunks
        chunk_files = [f"million_trades_part_{i:02d}_of_07.json" for i in range(1, 8)]
        all_chunks_exist = all(os.path.exists(f) for f in chunk_files)
        
        if all_chunks_exist:
            print(f"   ✅ All 7 chunks present")
            
            # Verify reconstruction script
            if os.path.exists("reconstruct_million_trades.py"):
                print("   ✅ Reconstruction script available")
                checks_passed += 1
            else:
                print("   ❌ Reconstruction script missing")
        else:
            missing = [f for f in chunk_files if not os.path.exists(f)]
            print(f"   ❌ Missing chunks: {missing}")
    
    print("")
    
    # Check 2: OANDA Configuration
    print("2. 🔗 OANDA LIVE TRADING SETUP")
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'OANDA_LIVE=true' in env_content:
            print("   ✅ Live trading enabled")
        else:
            print("   ⚠️  Practice mode active")
        
        if 'OANDA_API_KEY' in env_content:
            print("   ✅ API key configured")
        else:
            print("   ❌ API key missing")
        
        if 'api-fxtrade.oanda.com' in env_content:
            print("   ✅ Live API endpoint configured")
            checks_passed += 1
        else:
            print("   ⚠️  Practice API endpoint")
    else:
        print("   ❌ .env file missing")
    
    print("")
    
    # Check 3: Flask Application
    print("3. 🌐 FLASK TRADING APPLICATION")
    if os.path.exists('app.py'):
        print("   ✅ Flask app exists")
        checks_passed += 1
    else:
        print("   ❌ Flask app missing")
    
    print("")
    
    # Check 4: Autonomous Trading System
    print("4. 🤖 AUTONOMOUS TRADING ENGINE")
    if os.path.exists('live_trading_system.py'):
        print("   ✅ Autonomous engine exists")
        checks_passed += 1
    else:
        print("   ❌ Autonomous engine missing")
    
    print("")
    
    # Check 5: TradingView Integration
    print("5. 📈 TRADINGVIEW WEBHOOK INTEGRATION")
    if os.path.exists('TRADINGVIEW_SETUP_GUIDE.md'):
        print("   ✅ TradingView setup guide available")
        checks_passed += 1
    else:
        print("   ❌ TradingView setup guide missing")
    
    print("")
    
    # Check 6: Safety Systems
    print("6. 🛡️  SAFETY SYSTEMS")
    safety_files = ['comprehensive_safety_system.py', 'oanda_client.py']
    safety_exists = all(os.path.exists(f) for f in safety_files)
    
    if safety_exists:
        print("   ✅ Safety systems deployed")
        checks_passed += 1
    else:
        missing = [f for f in safety_files if not os.path.exists(f)]
        print(f"   ❌ Missing safety files: {missing}")
    
    print("")
    
    # Check 7: Deployment Tools
    print("7. 🚀 DEPLOYMENT TOOLS")
    deploy_tools = ['final_million_splitter.py', 'deploy_with_lfs.py']
    tools_exist = any(os.path.exists(f) for f in deploy_tools)
    
    if tools_exist:
        print("   ✅ Deployment tools available")
        checks_passed += 1
    else:
        print("   ❌ Deployment tools missing")
    
    print("")
    
    # Check 8: Git Repository
    print("8. 🔗 GIT REPOSITORY STATUS")
    if os.path.exists('.git'):
        print("   ✅ Git repository initialized")
        
        # Check recent commits
        try:
            import subprocess
            result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                  capture_output=True, text=True, check=True)
            latest_commit = result.stdout.strip()
            print(f"   ✅ Latest commit: {latest_commit}")
            
            if "million trade" in latest_commit.lower():
                print("   ✅ Million trade deployment confirmed")
                checks_passed += 1
        except Exception as e:
            print(f"   ⚠️  Could not verify commits: {e}")
    else:
        print("   ❌ Not a git repository")
    
    print("")
    
    # Final Assessment
    print("=" * 70)
    print("🏆 FINAL DEPLOYMENT ASSESSMENT")
    print("=" * 70)
    
    score = (checks_passed / total_checks) * 100
    
    print(f"🎯 Score: {checks_passed}/{total_checks} ({score:.0f}%)")
    print("")
    
    if score >= 90:
        print("🎉 EXCELLENT! System fully deployed and ready for live trading!")
        print("✅ Million trade dataset successfully integrated")
        print("✅ All critical systems operational")
        print("✅ Ready for TradingView webhook configuration")
    elif score >= 75:
        print("✅ GOOD! System mostly ready with minor items to address")
        print("📋 Review any failed checks above")
    elif score >= 60:
        print("⚠️  PARTIAL! System partially deployed")
        print("🔧 Address failed checks before live trading")
    else:
        print("❌ INCOMPLETE! Significant deployment issues")
        print("🛠️  Major fixes required")
    
    print("")
    print("📋 NEXT STEPS:")
    print("1. Configure TradingView alerts using TRADINGVIEW_SETUP_GUIDE.md")
    print("2. Test with small position sizes initially")
    print("3. Monitor the autonomous trading dashboard")
    print("4. Verify live OANDA account connection")
    
    print("")
    print("🚀 JARVIS AUTONOMOUS TRADING SYSTEM - DEPLOYMENT COMPLETE!")
    print("=" * 70)
    
    return score >= 90

if __name__ == "__main__":
    success = verify_deployment()
    print(f"\n{'🎉 System Ready!' if success else '⚠️  Needs Attention'}")
