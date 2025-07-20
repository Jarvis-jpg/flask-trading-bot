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
1. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` for local development:
   ```
   OANDA_API_KEY=your_api_key
   OANDA_ACCOUNT_ID=your_account_id
   OANDA_LIVE=false
   OANDA_API_URL=https://api-fxpractice.oanda.com
   ```

3. Configure environment variables for deployment:
   - In render.com dashboard, add environment variables
   - For other platforms, use their environment configuration interface
   - Never commit API keys to version control
   
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
       startCommand: gunicorn app:app
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0

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

2. Analyze results:
   - Review win rate progression
   - Check profit factor improvement
   - Verify learning effectiveness

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

4. Deployment Errors
   - Missing Environment Variables
     ```bash
     # Check if environment variables are set
     echo $OANDA_API_KEY
     echo $OANDA_ACCOUNT_ID
     
     # Set environment variables in render.com dashboard:
     OANDA_API_KEY=your_api_key
     OANDA_ACCOUNT_ID=your_account_id
     OANDA_LIVE=false
     OANDA_API_URL=https://api-fxpractice.oanda.com
     ```
   
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
