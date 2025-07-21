# Jarvis Trading Bot - System Manual

## Table of Contents
1. [System Overview](#system-overview)
2. [Initial Setup](#initial-setup)
3. [Startup Checklist](#startup-checklist)
4. [Monitoring and Maintenance](#monitoring-and-maintenance)
5. [Testing Procedures](#testing-procedures)
6. [Data Analysis and Learning](#data-analysis-and-learning)
7. [Troubleshooting](#troubleshooting)
8. [Emergency Procedures](#emergency-procedures)

## 1. System Overview

### Components
- Flask Web Server (app.py)
- Trade Analyzer (trade_analyzer.py)
- Model Trainer (model_trainer.py)
- OANDA Client (oanda_client.py)
- TradingView Integration (tradingview_client.py)

### Key Features
- Machine Learning-based trade analysis
- Continuous learning from trade results
- Real-time market analysis
- Risk management
- Performance tracking

## 2. Initial Setup

### Environment Setup
1. Install TA-Lib:
   
   Windows:
   ```bash
   # Download ta-lib-0.4.0-msvc.zip from:
   # http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip
   
   # Extract to C:\ta-lib
   
   # Add to System Environment Variables:
   # Path: C:\ta-lib\bin
   
   # Install Python wrapper:
   pip install TA-Lib
   ```
   
   Linux:
   ```bash
   wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   tar -xvf ta-lib-0.4.0-src.tar.gz
   cd ta-lib/
   ./configure --prefix=/usr
   make
   sudo make install
   pip install TA-Lib
   ```
   
   macOS:
   ```bash
   brew install ta-lib
   pip install TA-Lib
   ```

2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   
   Practice Mode (for development):
   ```
   OANDA_API_KEY=your_practice_api_key
   OANDA_ACCOUNT_ID=your_practice_account_id
   OANDA_LIVE=false
   OANDA_API_URL=https://api-fxpractice.oanda.com
   ```

   Live Trading Mode:
   ```
   OANDA_API_KEY=your_live_api_key
   OANDA_ACCOUNT_ID=your_live_account_id
   OANDA_LIVE=true
   OANDA_API_URL=https://api-fxtrade.oanda.com
   ```

   WARNING: Always verify these settings before deploying to production!

3. Configure environment variables for deployment:

   a. In render.com dashboard:
      - Go to Dashboard → Your Service → Environment
      - Add the following as "Secret Files":
        ```
        OANDA_API_KEY=your_api_key
        OANDA_ACCOUNT_ID=your_account_id
        ```
      - Ensure variables are marked as "Secret"
      - Values should not be visible in logs
   
   b. Verify environment setup:
      - Check Environment tab after deployment
      - Verify secrets are properly set
      - Monitor build logs for variable access
   
   c. Security best practices:
      - Never commit API keys to version control
      - Use different keys for development/production
      - Rotate keys periodically
      - Monitor for unauthorized access
   
4. Configure build environment:
   Create a `render.yaml` file:
   ```yaml
   services:
     - type: web
       name: trading-bot
       env: python
       buildCommand: |
         apt-get update && apt-get install -y python3-dev build-essential
         wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
         tar -xvf ta-lib-0.4.0-src.tar.gz
         cd ta-lib/ && ./configure --prefix=/usr && make && make install
         pip install -r requirements.txt
         # Fix oandapyV20 warnings
         sed -i 's/\\\[/\[/g' .venv/lib/python3.*/site-packages/oandapyV20/endpoints/decorators.py
         sed -i 's/\\{/{/g' .venv/lib/python3.*/site-packages/oandapyV20/endpoints/decorators.py
       startCommand: gunicorn app:app
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
         - key: OANDA_API_KEY
           sync: false
         - key: OANDA_ACCOUNT_ID
           sync: false
         - key: OANDA_LIVE
           value: "true"  # Changed to true for live trading
         - key: OANDA_API_URL
           value: "https://api-fxtrade.oanda.com"  # Changed to live API URL

3. Create required directories:
   ```bash
   mkdir data models logs
   ```

### Initial Model Training
1. Generate initial training data:
   ```bash
   python generate_training_data.py
   ```
   - Creates 8000 simulated trades
   - Trains initial model
   - Saves model to models/model.pkl

2. Verify model creation:
   - Check models/model.pkl exists
   - Check models/scaler.pkl exists
   - Review initial performance metrics

## 3. Startup Checklist

### Daily Startup Sequence
1. **System Check**
   - [ ] Check system disk space (min 1GB free)
   - [ ] Check data directory for corruption
   - [ ] Verify model files exist

2. **Connection Tests**
   - [ ] Run test_connection endpoint
   ```bash
   curl http://localhost:5000/test_connection
   ```
   - [ ] Verify OANDA connection
   - [ ] Verify TradingView webhook
   - [ ] Check market data feed

3. **Model Verification**
   - [ ] Load latest model
   - [ ] Check model performance metrics
   - [ ] Verify feature importance rankings

4. **Start Trading System**
   ```bash
   python app.py
   ```

### Pre-Trading Checks
- [ ] Verify account balance
- [ ] Check open positions
- [ ] Review risk limits
- [ ] Verify market hours
- [ ] Check economic calendar

## 4. Monitoring and Maintenance

### Daily Monitoring
1. **Performance Metrics**
   - Win rate
   - Profit factor
   - Average profit
   - Model accuracy

2. **System Health**
   - CPU usage
   - Memory usage
   - Response times
   - Error rates

3. **Trade Analysis**
   - Open positions
   - Pending orders
   - Risk exposure
   - P&L analysis

### Weekly Maintenance
1. **Data Cleanup**
   - Archive old logs
   - Compress trade history
   - Backup database

2. **Model Update**
   - Retrain model with new data
   - Compare performance metrics
   - Update feature importance

3. **System Updates**
   - Check for dependencies updates
   - Update API versions
   - Review security patches

## 5. Testing Procedures

### Regular Testing
1. **Connection Testing**
   ```bash
   python test_connection.py
   ```

2. **Model Testing**
   ```bash
   python adaptive_test_8000.py
   ```

3. **Strategy Testing**
   ```bash
   python test_strategies.py
   ```

### Performance Testing
1. Run batch tests:
   ```bash
   python test_8000.py
   ```

2. Run adaptive tests:
   ```bash
   # Standard run (takes ~15-20 minutes)
   python adaptive_test_8000.py

   # Quick test with minimal delay (for development)
   QUICK_TEST=1 python adaptive_test_8000.py

   # Background run (recommended for production)
   nohup python adaptive_test_8000.py > adaptive_test.log 2>&1 &
   ```

3. Test Duration Settings:
   - Default: 100ms delay between trades
   - Quick Test: 10ms delay (set QUICK_TEST=1)
   - No Delay: 0ms (set NO_DELAY=1)
   
   Note: Reducing delays may affect simulation realism

4. Analyze results:
   - Review win rate progression
   - Check profit factor improvement
   - Verify learning effectiveness
   - Monitor adaptive_test.log for progress

## 6. Data Analysis and Learning

### Data Collection
1. Trade Data
   - Entry/exit prices
   - Market conditions
   - Technical indicators
   - Trade outcomes

2. Performance Metrics
   - Win/loss ratios
   - Risk/reward ratios
   - Profit factors
   - Drawdown analysis

### Learning Process
1. **Daily Learning**
   - Update model with new trades
   - Calculate performance metrics
   - Adjust risk parameters
   - Update feature importance

2. **Weekly Analysis**
   - Review performance trends
   - Identify successful patterns
   - Analyze failed trades
   - Update trading rules

3. **Monthly Review**
   - Full model retraining
   - Strategy optimization
   - Risk management review
   - Performance reporting

### Performance Tracking
1. Monitor metrics in data/performance_history.csv:
   - Win rate progression
   - Profit factor trends
   - Average profit changes
   - Learning factor impact

2. Review feature importance:
   ```python
   model_trainer.feature_importance
   ```

## 7. Troubleshooting

### Common Issues
1. Connection Errors
   - Check API credentials
   - Verify network connection
   - Review API limits

2. Model Errors
   - Check data format
   - Verify feature engineering
   - Review model parameters

3. Trading Errors
   - Check account balance
   - Verify position limits
   - Review risk parameters

4. TA-Lib Issues
   - If you see "TA-Lib not available, using fallback calculations":
     * This means the system is using built-in fallback implementations
     * Performance may be slower
     * Some indicators might have slight calculation differences
   - Solutions:
     * Follow installation instructions in Environment Setup
     * Verify system architecture matches TA-Lib build
     * Check for conflicting dependencies

5. Testing Issues
   - Long Test Duration:
     * 8000 trades × 100ms = ~13.3 minutes minimum
     * Use QUICK_TEST=1 for faster testing
     * Use NO_DELAY=1 for instant execution (development only)
   
   - Test Interruption:
     * Ctrl+C interrupts generate KeyboardInterrupt
     * Use `nohup` or background execution for long tests
     * Check adaptive_test.log for progress
   
   - Memory Issues:
     * Monitor RAM usage during long tests
     * Consider reducing batch_size if needed
     * Use performance monitoring tools

6. Deployment Errors

   a. Environment Variable Issues:
      - Verify in render.com dashboard:
        ```bash
        # Check deployment logs for:
        "ValueError: OANDA_API_KEY and OANDA_ACCOUNT_ID environment variables must be set"
        
        # Solution: Add to Environment → Secret Files
        OANDA_API_KEY=your_api_key
        OANDA_ACCOUNT_ID=your_account_id
        ```
      - Ensure variables are marked as "Secret"
      - Redeploy after adding variables
   
   b. Python Version Conflicts:
      - Check for warnings like:
        ```
        SyntaxWarning: invalid escape sequence '\['
        ```
      - Fixed automatically in render.yaml build steps
      - Manual fix if needed:
        ```bash
        sed -i 's/\\\[/\[/g' path/to/decorators.py
        sed -i 's/\\{/{/g' path/to/decorators.py
        ```
   
   c. Build Process:
      - Check build logs for TA-Lib installation
      - Verify Python dependencies install correctly
      - Monitor gunicorn startup messages
      - Check for proper environment loading

   d. Trading Mode Verification:
      - Check current mode in render.com dashboard:
        ```bash
        # For live trading, environment should show:
        OANDA_LIVE=true
        OANDA_API_URL=https://api-fxtrade.oanda.com

        # If showing practice mode instead:
        OANDA_LIVE=false
        OANDA_API_URL=https://api-fxpractice.oanda.com
        ```
      - To switch to live trading:
        1. Update OANDA_LIVE to "true"
        2. Change API URL to live endpoint
        3. Use live account credentials
        4. Redeploy the application
      
      WARNING: Always double-check these settings before live trading!
   
   - TA-Lib Installation
     ```bash
     # Add to your render.yaml or build script:
     - apt-get update && apt-get install -y python3-dev build-essential
     - wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
     - tar -xvf ta-lib-0.4.0-src.tar.gz
     - cd ta-lib/ && ./configure --prefix=/usr && make && make install
     - pip install TA-Lib
     ```

### Error Recovery
1. Stop trading:
   ```bash
   curl http://localhost:5000/stop
   ```

2. Backup data:
   ```bash
   python backup_data.py
   ```

3. Restore system:
   ```bash
   python restore_system.py
   ```

## 8. Emergency Procedures

### Emergency Shutdown
1. Stop trading system:
   ```bash
   curl http://localhost:5000/emergency_stop
   ```

2. Close all positions:
   ```bash
   python close_all_positions.py
   ```

3. Save system state:
   ```bash
   python save_state.py
   ```

### Recovery Procedures
1. Verify data integrity
2. Check account status
3. Review error logs
4. Restart with reduced risk

### Contact Information
- System Administrator: [Contact]
- OANDA Support: [Contact]
- Emergency Support: [Contact]
