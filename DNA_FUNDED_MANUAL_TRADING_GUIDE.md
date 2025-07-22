# 🧬 MANUAL DNA FUNDED TRADING GUIDE
## Using JARVIS AI Signals with DNA Funded TradeLocker Platform

### 🎯 HYBRID TRADING STRATEGY OVERVIEW

Your JARVIS system will generate AI-powered trading signals, and you'll execute them manually on DNA Funded's TradeLocker platform. This combines the best of both worlds:

- **AI Analysis**: JARVIS provides sophisticated market analysis
- **Manual Execution**: You maintain full control over trade execution
- **Prop Firm Capital**: Access to up to $600k in funding

---

## 🔧 SETUP PROCESS

### Step 1: DNA Funded Account Setup
1. **Choose Challenge Size**
   ```
   Recommended: Start with $10,000 or $25,000 challenge
   Cost: $89 (10k) or $179 (25k)
   Profit Target: 10%
   Max Daily Loss: 5%
   Max Total Loss: 6%
   ```

2. **Purchase Challenge**
   - Go to dnafunded.com
   - Select challenge size
   - Complete payment
   - Receive TradeLocker credentials

3. **TradeLocker Access**
   ```
   Platform: TradeLocker (web-based)
   Login: live.tradelocker.com
   Demo credentials provided during signup
   ```

### Step 2: JARVIS Signal Generation Setup
1. **Keep OANDA Connection**
   ```bash
   # Your .env file stays the same
   OANDA_API_KEY=your_api_key_here
   OANDA_ACCOUNT_ID=your_account_id_here
   OANDA_LIVE=false  # Keep in practice mode
   ```

2. **Run JARVIS Dashboard**
   ```bash
   python start_trading_bot.py
   # Access dashboard at http://localhost:5000
   ```

3. **Configure for Signal-Only Mode**
   - JARVIS generates signals
   - No automatic execution
   - Manual copy to DNA Funded

---

## 📊 DAILY TRADING WORKFLOW

### Morning Routine (Market Open)
1. **Start JARVIS System**
   ```bash
   python start_trading_bot.py
   ```

2. **Open TradeLocker**
   - Login to DNA Funded account
   - Check account balance and status
   - Verify daily loss limits

3. **Monitor JARVIS Dashboard**
   - Check AI confidence levels
   - Review market conditions
   - Wait for high-quality signals

### Signal Processing Workflow

#### When JARVIS Generates a Signal:
1. **Signal Appears on Dashboard**
   ```
   Signal Example:
   Pair: EUR/USD
   Action: BUY
   Entry: 1.0950
   Stop Loss: 1.0920
   Take Profit: 1.1010
   Confidence: 85%
   Risk/Reward: 2:1
   ```

2. **Manual Validation Checklist**
   ```
   ✅ Confidence > 75%
   ✅ Risk/Reward > 1.5:1
   ✅ Within DNA Funded daily limits
   ✅ Market session aligns (London/NY overlap preferred)
   ✅ No major news events pending
   ```

3. **Calculate DNA Funded Position Size**
   ```
   DNA Funded Rules:
   - Max 5% daily loss
   - Max 6% total loss
   
   Position Sizing Formula:
   Risk Amount = Account Balance × 2% (conservative)
   Position Size = Risk Amount ÷ Stop Loss Distance (pips)
   
   Example with $10,000 account:
   Risk Amount = $10,000 × 2% = $200
   Stop Loss Distance = 30 pips
   Position Size = $200 ÷ 30 pips = 0.67 lots
   ```

4. **Execute on TradeLocker**
   - Open new order window
   - Select currency pair
   - Enter position size
   - Set entry price (market or limit)
   - Set stop loss
   - Set take profit
   - Confirm order

---

## 🎛️ TRADELOCKER EXECUTION GUIDE

### Order Entry Process
1. **Market Order (Immediate Execution)**
   ```
   1. Click "New Order"
   2. Select instrument (EUR/USD)
   3. Choose "Market" order type
   4. Enter volume (lot size)
   5. Set Stop Loss price
   6. Set Take Profit price
   7. Click "Place Order"
   ```

2. **Limit Order (Wait for Entry Price)**
   ```
   1. Click "New Order"
   2. Select instrument
   3. Choose "Limit" order type
   4. Enter target entry price
   5. Enter volume
   6. Set Stop Loss
   7. Set Take Profit
   8. Click "Place Order"
   ```

### Position Management
1. **Monitor Open Positions**
   - Check P&L in real-time
   - Watch for JARVIS exit signals
   - Monitor daily loss limits

2. **Manual Exit Options**
   ```
   - Close at Take Profit (automatic)
   - Close at Stop Loss (automatic)
   - Manual close on JARVIS signal
   - Emergency close if limits approached
   ```

---

## 📋 RISK MANAGEMENT FOR DNA FUNDED

### Daily Monitoring Checklist
```
Daily P&L Tracking:
□ Current daily P&L: _____
□ Max daily loss limit: -5% (-$500 for $10k account)
□ Remaining daily risk: _____
□ Number of trades today: _____
□ Win rate today: _____%
```

### Position Sizing Guidelines
```
Account Size | Max Risk Per Trade | Max Position Size
$5,000      | $100 (2%)         | 0.5 lots max
$10,000     | $200 (2%)         | 1.0 lots max
$25,000     | $500 (2%)         | 2.5 lots max
$50,000     | $1,000 (2%)       | 5.0 lots max
```

### Emergency Procedures
1. **Approaching Daily Loss Limit**
   ```
   If daily loss reaches -4%:
   - Stop all new trades
   - Close profitable positions
   - Reduce position sizes
   - Review strategy
   ```

2. **Technical Issues**
   ```
   If JARVIS system fails:
   - Switch to manual analysis
   - Use TradingView charts
   - Reduce position sizes
   - Focus on major pairs only
   ```

---

## 🔄 SIGNAL TRANSLATION PROCESS

### JARVIS Signal → TradeLocker Translation

#### Example 1: JARVIS Buy Signal
```
JARVIS Output:
Pair: GBP/USD
Action: BUY
Entry: 1.2650
Stop Loss: 1.2620
Take Profit: 1.2710
Confidence: 82%
Position Size: 10,000 units

TradeLocker Input:
Instrument: GBPUSD
Order Type: Market Buy
Volume: 0.10 lots (10,000 units)
Stop Loss: 1.2620
Take Profit: 1.2710
```

#### Example 2: JARVIS Sell Signal
```
JARVIS Output:
Pair: USD/JPY
Action: SELL
Entry: 150.80
Stop Loss: 151.20
Take Profit: 150.00
Confidence: 78%
Position Size: 5,000 units

TradeLocker Input:
Instrument: USDJPY
Order Type: Market Sell
Volume: 0.05 lots (5,000 units)
Stop Loss: 151.20
Take Profit: 150.00
```

---

## 📊 PERFORMANCE TRACKING

### Daily Trading Log Template
```
Date: ___________
Account Balance Start: $_______
Account Balance End: $_______
Daily P&L: $_______

TRADES:
Trade 1:
- Pair: _______
- JARVIS Signal Time: _______
- Execution Time: _______
- Entry: _______
- Exit: _______
- P&L: $_______
- JARVIS Confidence: _____%

Trade 2:
[Repeat format]

NOTES:
- Signal quality: _______
- Execution delays: _______
- Market conditions: _______
- Lessons learned: _______
```

### Weekly Review Process
1. **Analyze Performance Gap**
   ```
   Compare:
   - JARVIS simulated results
   - Actual DNA Funded results
   - Identify execution differences
   - Adjust timing/sizing
   ```

2. **Optimize Signal Selection**
   ```
   Focus on:
   - Signals with >80% confidence
   - Major pairs during overlap sessions
   - Clear trend/momentum setups
   - Avoid news-sensitive periods
   ```

---

## 🎯 SUCCESS OPTIMIZATION TIPS

### 1. Timing Optimization
```
Best Signal Execution Times:
- London/NY Overlap: 1:00-5:00 PM GMT
- Avoid Asian session (low volatility)
- Avoid major news releases
- Execute within 2-3 minutes of signal
```

### 2. Signal Quality Filters
```
Only Execute Signals With:
✅ Confidence > 75%
✅ Risk/Reward > 1.5:1
✅ Clear stop loss levels
✅ Major currency pairs
✅ Good market liquidity
```

### 3. Position Management
```
Entry: Follow JARVIS signals exactly
Management: 
- Trail stops on 50% profit
- Close early if signal reverses
- Never hold through weekends
Exit: Follow JARVIS or hit targets
```

---

## 📈 SCALING STRATEGY

### Challenge Progression
```
Phase 1: $10k Challenge
Target: Pass with 10% profit
Focus: Consistency and rule compliance
Risk: 1-2% per trade

Phase 2: $25k Challenge  
Target: Larger position sizes
Focus: Scaling JARVIS signals
Risk: 2% per trade

Phase 3: $50k+ Funded Account
Target: Professional trading
Focus: Multiple timeframes
Risk: 1.5% per trade (conservative)
```

### Multiple Account Strategy
```
Account 1: Conservative (60% allocation)
- Lower risk per trade
- High-confidence signals only
- Focus on consistency

Account 2: Aggressive (40% allocation)
- Higher risk per trade  
- More signals executed
- Focus on growth
```

---

## 🚨 COMPLIANCE & RULES

### DNA Funded Rule Adherence
```
✅ Never exceed 5% daily loss
✅ Never exceed 6% total loss
✅ Trade minimum 3 days
✅ No weekend holding (check rules)
✅ No news trading restrictions (verify)
✅ Follow lot size limits
✅ Maintain detailed records
```

### Record Keeping
```
Required Documentation:
- All trade entries and exits
- JARVIS signal screenshots
- Daily P&L calculations
- Rule compliance checks
- Performance analysis
```

---

## 🎯 FINAL RECOMMENDATIONS

### Week 1-2: Setup & Testing
- Open DNA Funded demo account
- Practice signal execution
- Test timing and accuracy
- Optimize workflow

### Week 3-4: Live Challenge
- Start with smallest challenge size
- Focus on rule compliance
- Execute only high-confidence signals
- Track performance vs JARVIS

### Month 2+: Scaling
- Increase challenge sizes
- Add multiple accounts
- Refine signal selection
- Build consistent profitability

---

## 💡 KEY SUCCESS FACTORS

1. **Speed**: Execute signals within 2-3 minutes
2. **Discipline**: Only trade high-confidence signals
3. **Risk Management**: Never exceed daily limits
4. **Consistency**: Follow JARVIS recommendations exactly
5. **Documentation**: Track everything for analysis

This hybrid approach gives you the best of both worlds - AI-powered analysis with human oversight and prop firm capital!
