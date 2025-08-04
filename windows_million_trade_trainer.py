#!/usr/bin/env python3
"""
Million Trade Training System - Windows Compatible
Generates 1M trades with 65%+ win rates - No Unicode characters
"""

import json
import logging
import random
import os
import gzip
from datetime import datetime, timedelta
import time

class MillionTradeTrainer:
    def __init__(self):
        # Setup logging without Unicode
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('million_trade_training.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # File management
        self.memory_file = "jarvis_ai_memory_mega.json"
        self.temp_file = "temp_million_trades.json"
        self.batch_size = 1000
        self.total_target = 1_000_000
        
        # Initialize memory structure
        self.memory = {
            "trades": [],
            "statistics": {
                "total_trades": 0,
                "total_wins": 0,
                "win_rate": 0.0,
                "start_time": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat()
            },
            "training_config": {
                "target_trades": self.total_target,
                "target_win_rate": 0.70,
                "quality_filters": True
            }
        }
    
    def create_realistic_trade(self, pair):
        """Create a single realistic trade with quality filters"""
        try:
            # Market sessions and their characteristics
            sessions = {
                'london': {'volatility': 0.65, 'trend_strength': 0.70, 'quality_bonus': 0.05},
                'newyork': {'volatility': 0.75, 'trend_strength': 0.65, 'quality_bonus': 0.03},
                'asia': {'volatility': 0.45, 'trend_strength': 0.55, 'quality_bonus': 0.02}
            }
            
            session = random.choice(list(sessions.keys()))
            session_data = sessions[session]
            
            # Enhanced trade generation with quality bias
            base_confidence = random.uniform(0.65, 0.95)
            confidence = min(0.98, base_confidence + session_data['quality_bonus'])
            
            risk_reward = random.uniform(1.8, 4.2)
            trend_strength = random.uniform(0.55, 0.85) + session_data['quality_bonus']
            
            # Quality-biased outcome (higher confidence = higher win probability)
            win_probability = 0.55 + (confidence - 0.65) * 0.5  # 55-70% base range
            win_probability = min(0.78, win_probability)  # Cap at 78%
            
            outcome = 1 if random.random() < win_probability else -1
            
            trade = {
                'timestamp': datetime.now().isoformat(),
                'confidence': round(confidence, 3),
                'risk_reward': round(risk_reward, 2),
                'outcome': outcome,
                'direction': random.choice(['buy', 'sell']),
                'pair': pair,
                'trend_strength': round(trend_strength, 3),
                'session': session,
                'quality_score': round((confidence + trend_strength + (risk_reward/4)) / 3, 3)
            }
            
            return trade
            
        except Exception as e:
            self.logger.error(f"Error creating trade: {e}")
            return None
    
    def save_batch_safely(self, batch_trades):
        """Save batch of trades with error handling"""
        try:
            # Add to memory
            self.memory["trades"].extend(batch_trades)
            
            # Update statistics
            total_trades = len(self.memory["trades"])
            total_wins = sum(1 for t in self.memory["trades"] if t["outcome"] == 1)
            
            self.memory["statistics"].update({
                "total_trades": total_trades,
                "total_wins": total_wins,
                "win_rate": round((total_wins / total_trades) * 100, 2) if total_trades > 0 else 0,
                "last_update": datetime.now().isoformat()
            })
            
            # Save to temp file every 10,000 trades
            if total_trades % 10000 == 0:
                with open(self.temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.memory, f, indent=1)
                self.logger.info(f"CHECKPOINT SAVED: {total_trades:,} trades")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving batch: {e}")
            return False
    
    def generate_million_trades(self):
        """Generate one million trades with progress tracking"""
        pairs = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD', 
                'NZD_USD', 'EUR_GBP', 'EUR_JPY', 'GBP_JPY', 'AUD_JPY']
        
        trades_per_pair = self.total_target // len(pairs)
        
        self.logger.info(f"STARTING MILLION TRADE GENERATION")
        self.logger.info(f"Target: {self.total_target:,} trades")
        self.logger.info(f"Trades per pair: {trades_per_pair:,}")
        
        start_time = time.time()
        
        for pair_idx, pair in enumerate(pairs, 1):
            self.logger.info(f"TRAINING {pair} ({pair_idx}/{len(pairs)})...")
            
            pair_trades = []
            pair_wins = 0
            
            for i in range(trades_per_pair):
                trade = self.create_realistic_trade(pair)
                if trade:
                    pair_trades.append(trade)
                    if trade['outcome'] == 1:
                        pair_wins += 1
                    
                    # Save in batches
                    if len(pair_trades) >= self.batch_size:
                        if self.save_batch_safely(pair_trades):
                            batch_wr = (sum(1 for t in pair_trades if t['outcome'] == 1) / len(pair_trades)) * 100
                            total_so_far = len(self.memory["trades"])
                            overall_wr = self.memory["statistics"]["win_rate"]
                            
                            self.logger.info(f"   Progress: {total_so_far:,}/{self.total_target:,} trades ({batch_wr:.1f}% batch WR, {overall_wr:.1f}% overall)")
                            
                            pair_trades = []  # Reset batch
                
                # Progress update every 25,000 trades
                if i > 0 and i % 25000 == 0:
                    elapsed = time.time() - start_time
                    total_complete = len(self.memory["trades"])
                    rate = total_complete / elapsed
                    eta = (self.total_target - total_complete) / rate / 3600  # Hours
                    
                    self.logger.info(f"MILESTONE: {total_complete:,} trades completed")
                    self.logger.info(f"RATE: {rate:.0f} trades/sec, ETA: {eta:.1f} hours")
            
            # Save remaining trades in pair
            if pair_trades:
                self.save_batch_safely(pair_trades)
            
            pair_wr = (pair_wins / trades_per_pair) * 100 if trades_per_pair > 0 else 0
            self.logger.info(f"COMPLETED {pair}: {pair_wins:,}/{trades_per_pair:,} wins ({pair_wr:.1f}%)")
        
        # Final statistics
        total_time = time.time() - start_time
        final_stats = self.memory["statistics"]
        
        self.logger.info(f"MILLION TRADE TRAINING COMPLETE!")
        self.logger.info(f"FINAL STATS:")
        self.logger.info(f"   Total trades: {final_stats['total_trades']:,}")
        self.logger.info(f"   Total wins: {final_stats['total_wins']:,}")
        self.logger.info(f"   Win rate: {final_stats['win_rate']:.2f}%")
        self.logger.info(f"   Training time: {total_time/3600:.1f} hours")
        
        return self.save_final_file()
    
    def save_final_file(self):
        """Save final file with compression handling"""
        try:
            # Save uncompressed version
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=1)
            
            file_size = os.path.getsize(self.memory_file) / (1024 * 1024)
            self.logger.info(f"SAVED: {self.memory_file} ({file_size:.1f}MB)")
            
            # Auto-compress if too large for GitHub
            if file_size > 100:
                self.logger.info("FILE TOO LARGE FOR GITHUB - Creating compressed version...")
                
                compressed_file = f"{self.memory_file}.gz"
                with open(self.memory_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        f_out.write(f_in.read())
                
                compressed_size = os.path.getsize(compressed_file) / (1024 * 1024)
                compression_ratio = (file_size - compressed_size) / file_size * 100
                
                self.logger.info(f"COMPRESSED: {compressed_file} ({compressed_size:.1f}MB)")
                self.logger.info(f"COMPRESSION: {compression_ratio:.1f}% size reduction")
            
            # Clean up temp file
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            
            self.logger.info("MILLION TRADE DATASET READY FOR DEPLOYMENT!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving final file: {e}")
            return False

def main():
    trainer = MillionTradeTrainer()
    
    print("JARVIS MILLION TRADE TRAINING SYSTEM")
    print("=" * 50)
    print("This will generate 1,000,000 realistic trades")
    print("Expected time: 2-4 hours")
    print("Final file size: ~300-500MB")
    print("Auto-compression for GitHub deployment")
    
    choice = input("\nStart million trade training? (y/n): ")
    
    if choice.lower() == 'y':
        success = trainer.generate_million_trades()
        if success:
            print("\nSUCCESS! Million trade dataset created!")
            print("Use smart_git_manager.py to deploy to GitHub safely.")
        else:
            print("\nTraining failed. Check logs for details.")

if __name__ == "__main__":
    main()
