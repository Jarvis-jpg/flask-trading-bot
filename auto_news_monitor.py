#!/usr/bin/env python3
"""
AUTO-START NEWS MONITORING SYSTEM
Automatically starts continuous monitoring without user input
"""

import requests
import json
import time
from datetime import datetime, timedelta

def fetch_news_sentiment():
    """Fetch and analyze current market news sentiment"""
    api_key = "e8b38405c48a48d2b62593732687a93b"
    
    # Financial keywords for forex/trading news
    keywords = [
        "USD", "EUR", "GBP", "JPY", "Federal Reserve", "ECB", "BOE", "BOJ",
        "interest rates", "inflation", "GDP", "employment", "trade war",
        "election", "Brexit", "cryptocurrency", "oil prices", "gold",
        "market crash", "recession", "stimulus", "quantitative easing"
    ]
    
    query = " OR ".join(keywords[:5])  # Limit to avoid URL length issues
    
    # Calculate time range (last 4 hours for forex relevance)
    now = datetime.now()
    from_time = (now - timedelta(hours=4)).strftime('%Y-%m-%dT%H:%M:%S')
    
    # NewsAPI endpoint for everything
    url = f"https://newsapi.org/v2/everything"
    params = {
        'apiKey': api_key,
        'q': query,
        'language': 'en',
        'sortBy': 'publishedAt',
        'from': from_time,
        'pageSize': 50
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'ok':
            print(f"❌ NewsAPI Error: {data.get('message', 'Unknown error')}")
            return 0.0, [], "ERROR"
        
        articles = data['articles']
        print(f"✅ Fetched {len(articles)} news articles")
        
        # Analyze sentiment
        sentiment_score = analyze_news_sentiment(articles)
        
        return sentiment_score, articles, "SUCCESS"
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return 0.0, [], "NETWORK_ERROR"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 0.0, [], "UNKNOWN_ERROR"

def analyze_news_sentiment(articles):
    """Analyze sentiment from news headlines and descriptions"""
    if not articles:
        return 0.0
    
    # Sentiment keywords with weights
    bullish_words = {
        'rally': 3, 'surge': 3, 'soar': 3, 'climb': 2, 'rise': 2, 'gain': 2,
        'boost': 2, 'strong': 2, 'positive': 2, 'optimistic': 2, 'growth': 2,
        'increase': 1, 'up': 1, 'higher': 1, 'bullish': 3, 'recovery': 2,
        'stimulus': 2, 'easing': 2, 'dovish': 2, 'cut rates': 3
    }
    
    bearish_words = {
        'crash': -4, 'plunge': -3, 'tumble': -3, 'fall': -2, 'drop': -2, 'decline': -2,
        'weak': -2, 'negative': -2, 'concern': -2, 'worry': -2, 'fear': -2,
        'crisis': -3, 'recession': -3, 'inflation': -2, 'hawkish': -2, 'raise rates': -3,
        'lower': -1, 'down': -1, 'bearish': -3, 'sell-off': -3, 'uncertainty': -2
    }
    
    total_score = 0
    article_count = 0
    
    for article in articles:
        if not article:
            continue
            
        # Combine title and description for analysis
        text = ""
        if article.get('title'):
            text += article['title'].lower() + " "
        if article.get('description'):
            text += article['description'].lower()
        
        if not text.strip():
            continue
            
        article_score = 0
        
        # Calculate sentiment score
        for word, weight in bullish_words.items():
            if word in text:
                article_score += weight
        
        for word, weight in bearish_words.items():
            if word in text:
                article_score += weight  # weight is already negative
        
        total_score += article_score
        article_count += 1
    
    if article_count == 0:
        return 0.0
    
    # Average and normalize to -20 to +20 range
    avg_score = total_score / article_count
    normalized_score = max(-20, min(20, avg_score * 2))
    
    return round(normalized_score, 1)

def generate_trading_recommendations(sentiment_score, article_count):
    """Generate trading recommendations based on news sentiment"""
    
    # Determine trading mode and settings
    if abs(sentiment_score) > 15:
        mode = "MAJOR EVENT"
        major_event = True
        risk_per_trade = 1.0
        min_signal = 65
        news_filter = True
    elif abs(sentiment_score) > 8:
        mode = "HIGH IMPACT"
        major_event = False
        risk_per_trade = 1.2
        min_signal = 60
        news_filter = True
    elif abs(sentiment_score) > 3:
        mode = "MODERATE"
        major_event = False
        risk_per_trade = 1.5
        min_signal = 55
        news_filter = True
    else:
        mode = "NORMAL"
        major_event = False
        risk_per_trade = 1.5
        min_signal = 55
        news_filter = False
    
    # Generate description
    if sentiment_score > 12:
        description = "VERY BULLISH - Strong positive news momentum"
    elif sentiment_score > 5:
        description = "BULLISH - Positive market sentiment"
    elif sentiment_score > 1:
        description = "SLIGHTLY BULLISH - Mild positive news"
    elif sentiment_score < -12:
        description = "VERY BEARISH - Strong negative news momentum"
    elif sentiment_score < -5:
        description = "BEARISH - Negative market sentiment"
    elif sentiment_score < -1:
        description = "SLIGHTLY BEARISH - Mild negative news"
    else:
        description = "NEUTRAL - Mixed or limited news impact"
    
    return {
        'news_bias': sentiment_score,
        'major_event_mode': major_event,
        'risk_per_trade': risk_per_trade,
        'min_signal_strength': min_signal,
        'news_filter': news_filter,
        'mode': mode,
        'description': description
    }

def continuous_monitoring():
    """Run continuous news monitoring every 30 minutes"""
    print("🚀 STARTING CONTINUOUS NEWS MONITORING")
    print("📊 Updates every 30 minutes")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            
            print(f"\n🔄 NEWS CYCLE #{cycle_count} - {current_time}")
            print("=" * 50)
            
            # Fetch news and analyze
            sentiment, articles, status = fetch_news_sentiment()
            
            if status == "SUCCESS":
                recommendations = generate_trading_recommendations(sentiment, len(articles))
                
                print(f"📊 News Sentiment: {sentiment:+.1f}")
                print(f"🎯 Trading Mode: {recommendations['mode']}")
                print(f"⚙️  Recommended Settings:")
                print(f"   • News Bias: {recommendations['news_bias']:+.1f}")
                print(f"   • Major Event: {recommendations['major_event_mode']}")
                print(f"   • Risk per Trade: {recommendations['risk_per_trade']}%")
                print(f"   • Min Signal: {recommendations['min_signal_strength']}")
                print(f"💡 {recommendations['description']}")
                
                print(f"\n🎯 CURRENT PINE SCRIPT SETTINGS:")
                print("Copy these values to your SevenSYS_Complete.pine inputs:")
                print(f"• News Sentiment Bias: {recommendations['news_bias']}")
                print(f"• Major Event Mode: {recommendations['major_event_mode']}")
                print(f"• Risk Per Trade: {recommendations['risk_per_trade']}%")
                print(f"• Min Signal Strength: {recommendations['min_signal_strength']}")
                print(f"• News Filter: {recommendations['news_filter']}")
                
                # Save to file for external access
                save_recommendations_to_file(recommendations)
                
            else:
                print(f"❌ Failed to fetch news: {status}")
                print("🔄 Will retry in next cycle")
            
            print(f"\n⏰ Next update in 30 minutes...")
            print("=" * 60)
            
            # Wait 30 minutes (1800 seconds)
            time.sleep(1800)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        print("👋 News monitoring shutdown complete")

def save_recommendations_to_file(recommendations):
    """Save current recommendations to JSON file for external access"""
    try:
        data = {
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }
        
        with open('current_news_settings.json', 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"⚠️  Warning: Could not save to file: {e}")

def main():
    print("📰 SEVENSYS AUTO-NEWS MONITORING SYSTEM")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Using your NewsAPI key: e8b38405c48a48d2b62593732687a93b")
    print()
    
    # Start continuous monitoring immediately
    continuous_monitoring()

if __name__ == "__main__":
    main()
