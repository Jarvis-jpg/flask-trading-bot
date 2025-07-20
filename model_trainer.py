import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_importance = {}
        self.performance_metrics = {
            'accuracy': [],
            'profit_factor': [],
            'win_rate': [],
            'avg_profit': []
        }
        self.required_features = [
            'trend', 'volatility', 'volume', 'rsi', 'macd_diff',
            'price_to_sma20', 'price_to_sma50', 'atr', 'cci',
            'risk_reward_ratio', 'hour_of_day'
        ]
        
    def prepare_data(self, trade_data: pd.DataFrame) -> tuple:
        """Prepare data for model training"""
        try:
            # Create a copy of the data
            df = trade_data.copy()
            
            # Remove any missing values
            df = df.dropna(subset=['profitable'])  # Only drop if target is missing
            
            # Ensure numeric columns are float type
            numeric_columns = ['volatility', 'volume', 'rsi', 'macd_diff',
                             'price_to_sma20', 'price_to_sma50', 'atr', 'cci',
                             'risk_reward_ratio']
            
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert hour_of_day to int
            df['hour_of_day'] = df['hour_of_day'].astype(int)
            
            # Convert trend to categorical and use one-hot encoding
            df['trend'] = df['trend'].astype('category')
            trend_dummies = pd.get_dummies(df['trend'], prefix='trend')
            
            # Prepare feature matrix
            features = numeric_columns + ['hour_of_day']
            X = pd.concat([df[features], trend_dummies], axis=1)
            
            # Debug information
            logger.info(f"DataFrame shape before feature extraction: {df.shape}")
            logger.info(f"Available columns: {df.columns.tolist()}")
            
            # Convert target to boolean
            y = df['profitable'].astype(bool)
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            logger.info(f"Final feature matrix shape: {X.shape}")
            logger.info(f"Final target vector shape: {y.shape}")
            
            return X_train_scaled, X_test_scaled, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
            
    def train_model(self, trade_data: pd.DataFrame) -> dict:
        """Train a new model on historical trade data"""
        try:
            logger.info("Starting model training...")
            
            # Prepare data
            X_train, X_test, y_train, y_test = self.prepare_data(trade_data)
            
            # Initialize and train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Calculate performance metrics
            train_accuracy = self.model.score(X_train, y_train)
            test_accuracy = self.model.score(X_test, y_test)
            
            # Calculate feature importance
            feature_names = (
                self.required_features[:-1] +  # All except 'trend'
                [f'trend_{cat}' for cat in ['uptrend', 'downtrend', 'sideways']]
            )
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Save model and scaler
            self.save_models()
            
            # Update performance metrics
            self.performance_metrics['accuracy'].append({
                'timestamp': datetime.now().isoformat(),
                'train_accuracy': train_accuracy,
                'test_accuracy': test_accuracy
            })
            
            return {
                'status': 'success',
                'train_accuracy': train_accuracy,
                'test_accuracy': test_accuracy,
                'feature_importance': feature_importance.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def update_model(self, new_trade_data: pd.DataFrame):
        """Update existing model with new trade data"""
        try:
            # Load existing training data
            historical_data = pd.read_csv('data/historical_trades.csv')
            
            # Calculate performance metrics for new trades
            new_trade_metrics = {
                'win_rate': (new_trade_data['profitable'].astype(bool).mean() * 100),
                'avg_profit': new_trade_data['profit'].mean(),
                'profit_factor': (
                    abs(new_trade_data[new_trade_data['profit'] > 0]['profit'].sum()) /
                    abs(new_trade_data[new_trade_data['profit'] < 0]['profit'].sum())
                    if len(new_trade_data[new_trade_data['profit'] < 0]) > 0 else float('inf')
                )
            }
            
            # Update performance metrics
            self.performance_metrics['win_rate'].append({
                'timestamp': datetime.now().isoformat(),
                'value': new_trade_metrics['win_rate']
            })
            self.performance_metrics['avg_profit'].append({
                'timestamp': datetime.now().isoformat(),
                'value': new_trade_metrics['avg_profit']
            })
            self.performance_metrics['profit_factor'].append({
                'timestamp': datetime.now().isoformat(),
                'value': new_trade_metrics['profit_factor']
            })
            
            # Append new data and remove duplicates
            updated_data = pd.concat([historical_data, new_trade_data]).drop_duplicates()
            
            # Retrain model
            result = self.train_model(updated_data)
            
            # Add performance metrics to result
            result['performance_metrics'] = new_trade_metrics
            
            # Save updated data
            updated_data.to_csv('data/historical_trades.csv', index=False)
            
            logger.info(f"Model updated with {len(new_trade_data)} new trades")
            logger.info(f"New performance metrics: {new_trade_metrics}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error updating model: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def save_models(self):
        """Save trained model and scaler"""
        try:
            os.makedirs('models', exist_ok=True)
            joblib.dump(self.model, 'models/model.pkl')
            joblib.dump(self.scaler, 'models/scaler.pkl')
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
            raise
    
    def evaluate_trade(self, features: pd.DataFrame) -> dict:
        """Evaluate a potential trade using the current model"""
        try:
            if self.model is None or self.scaler is None:
                raise ValueError("Model or scaler not initialized")
            
            # Prepare features in the same way as training data
            numeric_columns = ['volatility', 'volume', 'rsi', 'macd_diff',
                             'price_to_sma20', 'price_to_sma50', 'atr', 'cci',
                             'risk_reward_ratio']
            
            # Convert numeric features
            for col in numeric_columns:
                if col in features.columns:
                    features[col] = pd.to_numeric(features[col], errors='coerce')
            
            # Handle trend with one-hot encoding
            trend_dummies = pd.get_dummies(features['trend'], prefix='trend')
            
            # Combine features
            X = pd.concat([features[numeric_columns + ['hour_of_day']], trend_dummies], axis=1)
            
            # Scale features
            features_scaled = self.scaler.transform(X)
            
            # Get prediction and probability
            prediction = self.model.predict(features_scaled)[0]
            probability = self.model.predict_proba(features_scaled)[0][1]
            
            return {
                'recommended': prediction == 1,
                'confidence': float(probability),
                'threshold': 0.6  # Minimum confidence required
            }
            
        except Exception as e:
            logger.error(f"Error evaluating trade: {str(e)}")
            return {
                'error': str(e),
                'recommended': False,
                'confidence': 0.0
            }
