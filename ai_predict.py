import numpy as np
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def get_market_features(trade_data):
    """Extract meaningful features from trade data"""
    try:
        entry = float(trade_data['entry'])
        sl = float(trade_data['stop_loss'])
        tp = float(trade_data['take_profit'])
        
        features = {
            'risk_reward_ratio': abs(tp - entry) / abs(sl - entry),
            'stop_loss_distance': abs(sl - entry),
            'take_profit_distance': abs(tp - entry),
            'confidence': float(trade_data['confidence']),
            'hour_of_day': datetime.now().hour,
        }
        return features
    except Exception as e:
        print(f"❌ Error extracting features: {e}")
        return None

def predict_trade_outcome(trade_data):
    try:
        # Get features
        features = get_market_features(trade_data)
        if not features:
            return 'unknown', 0.0
            
        # Try to load the trained model
        try:
            model = joblib.load('model.pkl')
        except FileNotFoundError:
            # If no model exists, fall back to random prediction
            print("⚠️ No trained model found, using random prediction")
            return np.random.choice(['win', 'loss']), round(np.random.uniform(0.6, 0.9), 2)
            
        # Prepare features for prediction
        feature_df = pd.DataFrame([features])
        
        # Get prediction and probability
        prediction = model.predict(feature_df)[0]
        probabilities = model.predict_proba(feature_df)[0]
        confidence_score = round(max(probabilities), 2)
        
        result = 'win' if prediction == 1 else 'loss'
        
        return result, confidence_score
        
    except Exception as e:
        print(f"❌ Error in predict_trade_outcome: {e}")
        return 'unknown', 0.0

def analyze_trade(trade_result):
    """
    Analyze trade results and store metrics for ML model improvement
    """
    try:
        timestamp = datetime.now().isoformat()
        
        # Extract more meaningful metrics
        features = get_market_features(trade_result)
        analysis = {
            "timestamp": timestamp,
            "pair": trade_result["pair"],
            "action": trade_result["action"],
            "entry": trade_result["entry"],
            "prediction": trade_result["prediction"],
            "confidence": trade_result["confidence"],
            "risk_reward_ratio": features['risk_reward_ratio'],
            "stop_loss_distance": features['stop_loss_distance'],
            "take_profit_distance": features['take_profit_distance'],
            "hour_of_day": features['hour_of_day']
        }
        
        # Retrain model with new data
        if trade_result.get("result") in ["won", "lost"]:
            print("🔄 Triggering model retraining with new data...")
            from analyze_and_learn import analyze_and_learn
            analyze_and_learn()
        
        print(f"📊 Trade analysis complete: {analysis}")
        return analysis
        
    except Exception as e:
        print(f"❌ Error analyzing trade: {e}")
        return None