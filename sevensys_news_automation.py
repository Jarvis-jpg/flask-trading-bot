#!/usr/bin/env python3
"""
AUTOMATED NEWS INTEGRATION FOR SEVENSYS
Real-time news analysis with API integration
Updates Pine script parameters automatically
"""

import requests
import json
import time
from datetime import datetime, timedelta
import threading
import schedule

class SevenSYSNewsAutomation:
    def __init__(self):
        self.newsapi_key = "e8b38405c48a48d2b62593732687a93b"
        self.current_bias = 0.0
        self.last_update = None
        self.running = False
        
        # Enhanced keyword analysis
        self.market_keywords = {
            'very_bullish': {
                'keywords': ['trump elected', 'republican sweep', 'tax cuts approved', 'rate cut confirmed', 
                           'massive stimulus', 'crypto etf approved', 'peace agreement', 'inflation drops'],
                'weight': 4.0
            },
            'bullish': {
                'keywords': ['gdp growth', 'job gains', 'earnings beat', 'dovish fed', 'bull market', 
                           'business friendly', 'deregulation', 'market rally'],
                'weight': 2.0
            },
            'neutral_positive': {
                'keywords': ['stable growth', 'market steady', 'slight gains', 'cautious optimism'],
                'weight': 1.0
            },
            'neutral_negative': {
                'keywords': ['mixed signals', 'uncertain outlook', 'sideways market', 'wait and see'],
                'weight': -1.0
            },
            'bearish': {
                'keywords': ['rate hike', 'hawkish fed', 'earnings miss', 'recession fears', 
                           'bear market', 'regulation concerns', 'trade war'],
                'weight': -2.0
            },
            'very_bearish': {
                'keywords': ['market crash', 'economic crisis', 'war declared', 'major hack', 
                           'banking crisis', 'emergency measures', 'extreme volatility'],
                'weight': -4.0
            }
        }
        
    def fetch_live_news(self):
        """Fetch real-time news from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': '(market OR trading OR stocks OR forex OR fed OR trump OR bitcoin OR "federal reserve" OR election) AND (bullish OR bearish OR rally OR crash OR rate OR inflation)',
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 30,
                'from': (datetime.now() - timedelta(hours=6)).isoformat(),
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"✅ Fetched {len(articles)} news articles")
                return articles
            else:
                print(f"❌ API Error: {response.status_code}")
                return self._get_fallback_news()
                
        except Exception as e:
            print(f"⚠️  Error fetching news: {e}")
            return self._get_fallback_news()
    
    def _get_fallback_news(self):
        """Fallback news when API fails"""
        return [
            {
                'title': 'Markets Show Mixed Signals Amid Economic Data',
                'description': 'Traders await Fed decision as markets consolidate',
                'publishedAt': datetime.now().isoformat(),
                'source': {'name': 'Market Watch'}
            }
        ]
    
    def analyze_news_impact(self, articles):
        """Advanced news sentiment analysis"""
        total_score = 0.0
        article_count = 0
        impact_events = []
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = f"{title} {description}"
            
            article_score = 0.0
            matched_category = 'neutral'
            
            # Check each category
            for category, data in self.market_keywords.items():
                keywords = data['keywords']
                weight = data['weight']
                
                matches = sum(1 for keyword in keywords if keyword in content)
                if matches > 0:
                    category_score = matches * weight
                    if abs(category_score) > abs(article_score):
                        article_score = category_score
                        matched_category = category
            
            # Time decay - newer articles have more impact
            published = article.get('publishedAt', '')
            try:
                pub_time = datetime.fromisoformat(published.replace('Z', '+00:00'))
                hours_old = (datetime.now(pub_time.tzinfo) - pub_time).total_seconds() / 3600
                time_factor = max(0.1, 1.0 - (hours_old / 24.0))  # Decay over 24 hours
                article_score *= time_factor
            except:
                time_factor = 0.5  # Default if time parsing fails
            
            total_score += article_score
            article_count += 1
            
            # Track significant events
            if abs(article_score) > 2.0:
                impact_events.append({
                    'title': article.get('title', ''),
                    'score': article_score,
                    'category': matched_category,
                    'time_factor': time_factor
                })
        
        # Normalize score
        if article_count > 0:
            normalized_score = total_score / article_count
            # Cap at reasonable limits
            final_bias = max(-15.0, min(15.0, normalized_score * 3.0))
        else:
            final_bias = 0.0
        
        return final_bias, impact_events
    
    def determine_trading_mode(self, bias, impact_events):
        """Determine if major event mode should be activated"""
        major_event = False
        risk_adjustment = 1.0
        
        # Check for major events
        high_impact_count = len([e for e in impact_events if abs(e['score']) > 3.0])
        recent_high_impact = len([e for e in impact_events if abs(e['score']) > 2.5 and e['time_factor'] > 0.8])
        
        if abs(bias) > 10.0 or high_impact_count >= 2 or recent_high_impact >= 1:
            major_event = True
            risk_adjustment = 0.7  # Reduce risk during major events
        
        return major_event, risk_adjustment
    
    def generate_pine_settings(self, bias, major_event, risk_adj):
        """Generate settings for Pine script"""
        settings = {
            'news_bias': round(bias, 1),
            'major_event_mode': major_event,
            'risk_per_trade': round(1.5 * risk_adj, 1),
            'min_signal_strength': 60.0 if major_event else 55.0,
            'news_filter': True if abs(bias) > 2.0 else False,
        }
        
        # Determine recommendation
        if bias > 8.0:
            settings['recommendation'] = 'VERY_BULLISH - Strong positive sentiment'
        elif bias > 3.0:
            settings['recommendation'] = 'BULLISH - Positive market news'
        elif bias < -8.0:
            settings['recommendation'] = 'VERY_BEARISH - Strong negative sentiment'
        elif bias < -3.0:
            settings['recommendation'] = 'BEARISH - Negative market news'
        else:
            settings['recommendation'] = 'NEUTRAL - Mixed or limited news impact'
        
        return settings
    
    def save_settings(self, settings, impact_events):
        """Save settings to JSON file for external use"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'settings': settings,
            'impact_events': impact_events[:5],  # Top 5 events
            'last_bias': self.current_bias,
            'api_status': 'active'
        }
        
        with open('sevensys_news_settings.json', 'w') as f:
            json.dump(output, f, indent=2)
    
    def update_cycle(self):
        """Single update cycle"""
        print(f"\n🔄 NEWS UPDATE - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        # Fetch and analyze news
        articles = self.fetch_live_news()
        bias, impact_events = self.analyze_news_impact(articles)
        major_event, risk_adj = self.determine_trading_mode(bias, impact_events)
        
        # Generate settings
        settings = self.generate_pine_settings(bias, major_event, risk_adj)
        
        # Save for external access
        self.save_settings(settings, impact_events)
        
        # Update internal state
        self.current_bias = bias
        self.last_update = datetime.now()
        
        # Display results
        print(f"📊 News Sentiment: {bias:+.1f}")
        print(f"🎯 Trading Mode: {'MAJOR EVENT' if major_event else 'NORMAL'}")
        print(f"⚙️  Recommended Settings:")
        print(f"   • News Bias: {settings['news_bias']:+.1f}")
        print(f"   • Major Event: {settings['major_event_mode']}")
        print(f"   • Risk per Trade: {settings['risk_per_trade']:.1f}%")
        print(f"   • Min Signal: {settings['min_signal_strength']:.0f}")
        print(f"💡 {settings['recommendation']}")
        
        if impact_events:
            print(f"\n📰 Top Impact Events:")
            for i, event in enumerate(impact_events[:3], 1):
                print(f"   {i}. {event['title'][:60]}...")
                print(f"      Score: {event['score']:+.1f}, Category: {event['category']}")
        
        return settings
    
    def start_monitoring(self, interval_minutes=30):
        """Start continuous monitoring"""
        print("🚀 STARTING SEVENSYS NEWS MONITORING")
        print("=" * 50)
        print(f"Update Interval: {interval_minutes} minutes")
        print("Press Ctrl+C to stop")
        
        self.running = True
        
        try:
            # Initial update
            self.update_cycle()
            
            # Schedule regular updates
            schedule.every(interval_minutes).minutes.do(self.update_cycle)
            
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping news monitoring...")
            self.running = False
    
    def get_current_settings(self):
        """Get current settings for manual use"""
        if self.last_update is None:
            return self.update_cycle()
        
        # Return cached settings if recent (< 30 minutes)
        if (datetime.now() - self.last_update).total_seconds() < 1800:
            try:
                with open('sevensys_news_settings.json', 'r') as f:
                    data = json.load(f)
                    return data['settings']
            except:
                pass
        
        # Update if stale
        return self.update_cycle()

def main():
    news_system = SevenSYSNewsAutomation()
    
    print("📰 SEVENSYS AUTOMATED NEWS INTEGRATION")
    print("=" * 60)
    print("🔑 Using your NewsAPI key: e8b38405c48a48d2b62593732687a93b")
    print()
    
    # Get current settings
    current_settings = news_system.get_current_settings()
    
    print("\n🎯 CURRENT PINE SCRIPT SETTINGS:")
    print("Copy these values to your SevenSYS_Complete.pine inputs:")
    print(f"• News Sentiment Bias: {current_settings['news_bias']}")
    print(f"• Major Event Mode: {current_settings['major_event_mode']}")
    print(f"• Risk Per Trade: {current_settings['risk_per_trade']}%")
    print(f"• Min Signal Strength: {current_settings['min_signal_strength']}")
    print(f"• News Filter: {current_settings['news_filter']}")
    
    print("\n" + "="*60)
    print("OPTIONS:")
    print("1. Run once (get current settings)")
    print("2. Start continuous monitoring (every 30 minutes)")
    print("3. Quick monitoring (every 15 minutes)")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "2":
        news_system.start_monitoring(30)
    elif choice == "3":
        news_system.start_monitoring(15)
    else:
        print("✅ Current settings generated!")
        print("Check sevensys_news_settings.json for details")

if __name__ == "__main__":
    main()
