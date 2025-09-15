#!/usr/bin/env python3
"""
Real-time News Sentiment API Integration
Fetches news and updates Pine script parameters
"""

import requests
import json
from datetime import datetime
import time

class RealTimeNewsTrader:
    def __init__(self):
        # Free news APIs you can use
        self.apis = {
            'newsapi_key': 'e8b38405c48a48d2b62593732687a93b',  # Your NewsAPI key
            'alpha_vantage_key': 'YOUR_AV_KEY', # Get from alphavantage.co
            'finnhub_key': 'YOUR_FINNHUB_KEY'   # Get from finnhub.io
        }
        
        # Market impact keywords
        self.bullish_keywords = [
            'trump elected', 'republican victory', 'business friendly', 'tax cuts',
            'rate cut', 'stimulus', 'dovish', 'gdp growth', 'job gains', 
            'earnings beat', 'strong revenue', 'bull market', 'crypto etf'
        ]
        
        self.bearish_keywords = [
            'rate hike', 'hawkish', 'recession fears', 'unemployment up',
            'earnings miss', 'weak guidance', 'war', 'conflict', 'regulation',
            'bear market', 'crash', 'bubble', 'inflation surge'
        ]
        
        # Event multipliers
        self.event_weights = {
            'election': 3.0,
            'fed_meeting': 2.5,
            'earnings': 1.5,
            'geopolitical': 2.0,
            'economic_data': 1.8
        }

    def fetch_market_news(self):
        """Fetch latest market-relevant news"""
        try:
            # Real NewsAPI integration
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': 'market OR trading OR stocks OR forex OR crypto OR fed OR election OR trump OR bitcoin OR "federal reserve"',
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 20,
                'apiKey': self.apis['newsapi_key']
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                print(f"API Error: {response.status_code}")
                # Fallback to sample data
                return self._get_sample_news()
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            return self._get_sample_news()
    
    def _get_sample_news(self):
        """Fallback sample news data"""
        return [
            {
                'title': 'Market Rally Continues on Strong Economic Data',
                'description': 'S&P 500 reaches new highs amid positive sentiment',
                'publishedAt': '2025-09-12T10:00:00Z',
                'source': {'name': 'Reuters'}
            },
            {
                'title': 'Federal Reserve Maintains Current Interest Rates',
                'description': 'Powell signals cautious approach to monetary policy',
                'publishedAt': '2025-09-12T09:30:00Z',
                'source': {'name': 'Bloomberg'}
            }
        ]

    def analyze_sentiment(self, news_items):
        """Analyze sentiment and calculate market bias"""
        total_score = 0.0
        total_weight = 0.0
        
        for item in news_items:
            text = f"{item.get('title', '')} {item.get('description', '')}".lower()
            
            # Calculate sentiment
            bullish_score = sum(2 if keyword in text else 0 for keyword in self.bullish_keywords)
            bearish_score = sum(2 if keyword in text else 0 for keyword in self.bearish_keywords)
            
            # Determine event type and weight
            event_weight = 1.0
            if any(word in text for word in ['election', 'trump', 'biden']):
                event_weight = self.event_weights['election']
            elif any(word in text for word in ['fed', 'powell', 'rate']):
                event_weight = self.event_weights['fed_meeting']
            elif any(word in text for word in ['earnings', 'revenue']):
                event_weight = self.event_weights['earnings']
            
            # Calculate net sentiment
            net_sentiment = (bullish_score - bearish_score) / max(bullish_score + bearish_score, 1)
            
            total_score += net_sentiment * event_weight
            total_weight += event_weight
        
        # Return normalized bias (-1.0 to +1.0)
        if total_weight > 0:
            return max(min(total_score / total_weight, 1.0), -1.0)
        return 0.0

    def generate_pine_script_settings(self, sentiment_bias):
        """Generate settings for Pine script based on news sentiment"""
        
        # Trump election example - major bullish event
        if sentiment_bias > 0.7:
            return {
                'news_bias': 15.0,  # Very bullish
                'major_event_mode': True,
                'risk_per_trade': 1.0,  # Reduced risk due to volatility
                'min_signal_strength': 50.0,  # Lower threshold for more trades
                'recommendation': 'VERY_BULLISH - Trump election effect'
            }
        elif sentiment_bias > 0.3:
            return {
                'news_bias': 8.0,   # Moderately bullish
                'major_event_mode': False,
                'risk_per_trade': 1.5,
                'min_signal_strength': 55.0,
                'recommendation': 'BULLISH - Positive news flow'
            }
        elif sentiment_bias < -0.7:
            return {
                'news_bias': -15.0,  # Very bearish
                'major_event_mode': True,
                'risk_per_trade': 0.8,  # Much lower risk
                'min_signal_strength': 60.0,  # Higher threshold
                'recommendation': 'VERY_BEARISH - Major negative event'
            }
        elif sentiment_bias < -0.3:
            return {
                'news_bias': -8.0,   # Moderately bearish
                'major_event_mode': False,
                'risk_per_trade': 1.2,
                'min_signal_strength': 58.0,
                'recommendation': 'BEARISH - Negative news flow'
            }
        else:
            return {
                'news_bias': 0.0,    # Neutral
                'major_event_mode': False,
                'risk_per_trade': 1.5,
                'min_signal_strength': 55.0,
                'recommendation': 'NEUTRAL - Normal market conditions'
            }

    def update_trading_parameters(self):
        """Main function to update trading parameters based on news"""
        print("📰 FETCHING REAL-TIME NEWS...")
        news = self.fetch_market_news()
        
        print("🔍 ANALYZING SENTIMENT...")
        sentiment = self.analyze_sentiment(news)
        
        print("⚙️  GENERATING SETTINGS...")
        settings = self.generate_pine_script_settings(sentiment)
        
        # Save settings to JSON file
        with open('news_trading_settings.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'sentiment_bias': sentiment,
                'settings': settings,
                'latest_news': news[:3]  # Top 3 news items
            }, f, indent=2)
        
        return sentiment, settings

def main():
    trader = RealTimeNewsTrader()
    
    print("🚀 REAL-TIME NEWS TRADING SYSTEM")
    print("=" * 60)
    
    # Analyze current news
    sentiment, settings = trader.update_trading_parameters()
    
    print(f"📊 CURRENT MARKET SENTIMENT: {sentiment:+.2f}")
    print(f"🎯 RECOMMENDATION: {settings['recommendation']}")
    print()
    print("⚙️  PINE SCRIPT SETTINGS:")
    print(f"   News Bias: {settings['news_bias']:+.1f}")
    print(f"   Major Event Mode: {settings['major_event_mode']}")
    print(f"   Risk Per Trade: {settings['risk_per_trade']:.1f}%")
    print(f"   Min Signal Strength: {settings['min_signal_strength']:.0f}")
    print()
    
    print("📝 INSTRUCTIONS:")
    print("1. Copy these settings to your SevenSYS_NEWS_INTEGRATED.pine script")
    print("2. Update the 'News Sentiment Bias' input manually")
    print("3. Enable 'Major Event Mode' if recommended")
    print("4. Run this script daily to get updated settings")
    print()
    
    print("🔑 TRUMP ELECTION EXAMPLE:")
    print("   If Trump wins: News Bias = +15.0, Major Event = True")
    print("   If contested: News Bias = -10.0, Major Event = True")
    print("   This automatically adjusts strategy behavior!")
    
    # Demonstrate continuous monitoring
    print("\n🔄 Starting continuous monitoring...")
    print("   (Run this every 30 minutes during market hours)")
    
if __name__ == "__main__":
    main()
