"""
Real-Time Data Integration for Monte Carlo Simulations
This module provides integration with real-time market data sources and
automated parameter updates for dynamic simulations.
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class RealTimeDataIntegration:
    """Integration with real-time market data providers"""
    
    def __init__(self):
        self.data_sources = {
            'yahoo_finance': YahooFinanceAPI(),
            'alpha_vantage': AlphaVantageAPI(),
            'mock_data': MockDataProvider()  # Fallback for testing
        }
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 300  # 5 minutes cache
    
    def fetch_real_time_data(self, symbols: List[str]) -> Dict:
        """
        Fetch real-time market data for multiple symbols
        
        Parameters:
        symbols: List of stock symbols
        
        Returns:
        Dictionary with real-time data
        """
        data = {}
        
        for symbol in symbols:
            # Check cache first
            if self._is_cached(symbol):
                data[symbol] = self.cache[symbol]
                continue
            
            # Try different data sources
            for source_name, source in self.data_sources.items():
                try:
                    symbol_data = source.get_real_time_data(symbol)
                    if symbol_data:
                        data[symbol] = symbol_data
                        self._cache_data(symbol, symbol_data)
                        break
                except Exception as e:
                    print(f"⚠️ {source_name} failed for {symbol}: {e}")
                    continue
            
            if symbol not in data:
                print(f"❌ Could not fetch data for {symbol}")
        
        return data
    
    def _is_cached(self, symbol: str) -> bool:
        """Check if data is cached and not expired"""
        if symbol not in self.cache:
            return False
        
        if symbol not in self.cache_expiry:
            return False
        
        return datetime.now() < self.cache_expiry[symbol]
    
    def _cache_data(self, symbol: str, data: Dict):
        """Cache data with expiry time"""
        self.cache[symbol] = data
        self.cache_expiry[symbol] = datetime.now() + timedelta(seconds=self.cache_duration)
    
    def update_simulation_parameters(self, real_time_data: Dict) -> Dict:
        """
        Update simulation parameters based on real-time data
        
        Parameters:
        real_time_data: Real-time market data
        
        Returns:
        Updated parameters dictionary
        """
        if not real_time_data:
            return {}
        
        # Calculate market-wide metrics
        all_returns = []
        all_volatilities = []
        
        for symbol, data in real_time_data.items():
            if 'return' in data:
                all_returns.append(data['return'])
            if 'volatility' in data:
                all_volatilities.append(data['volatility'])
        
        if not all_returns or not all_volatilities:
            return {}
        
        # Calculate adjustments
        avg_return = np.mean(all_returns)
        avg_volatility = np.mean(all_volatilities)
        
        # Market sentiment analysis
        sentiment = self._analyze_market_sentiment(real_time_data)
        
        # Correlation updates
        correlation_matrix = self._update_correlations(real_time_data)
        
        return {
            'return_adjustment': avg_return,
            'volatility_adjustment': avg_volatility,
            'sentiment_factor': sentiment,
            'correlation_matrix': correlation_matrix,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_market_sentiment(self, data: Dict) -> float:
        """Analyze market sentiment from real-time data"""
        # Simple sentiment based on volume and price movements
        positive_changes = 0
        negative_changes = 0
        
        for symbol, symbol_data in data.items():
            if 'change' in symbol_data:
                if symbol_data['change'] > 0:
                    positive_changes += 1
                elif symbol_data['change'] < 0:
                    negative_changes += 1
        
        total_changes = positive_changes + negative_changes
        if total_changes == 0:
            return 0.5  # Neutral
        
        sentiment = positive_changes / total_changes
        return sentiment
    
    def _update_correlations(self, data: Dict) -> Optional[np.ndarray]:
        """Update correlation matrix based on recent data"""
        # This would typically use historical correlation data
        # For now, return a simplified correlation matrix
        n_assets = len(data)
        if n_assets < 2:
            return None
        
        # Create a basic correlation matrix
        correlations = np.eye(n_assets)
        
        # Add some correlation based on market sentiment
        for i in range(n_assets):
            for j in range(i+1, n_assets):
                # Simplified correlation calculation
                correlations[i, j] = correlations[j, i] = 0.3 + np.random.normal(0, 0.1)
        
        return correlations


class YahooFinanceAPI:
    """Yahoo Finance API integration"""
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Get real-time data from Yahoo Finance"""
        try:
            # Using yfinance-style endpoint (simplified)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_yahoo_data(data, symbol)
            
        except Exception as e:
            print(f"Yahoo Finance API error: {e}")
        
        return None
    
    def _parse_yahoo_data(self, data: Dict, symbol: str) -> Dict:
        """Parse Yahoo Finance response"""
        try:
            chart = data['chart']['result'][0]
            meta = chart['meta']
            
            # Calculate recent return
            current_price = meta['regularMarketPrice']
            previous_close = meta['previousClose']
            daily_return = (current_price - previous_close) / previous_close
            
            return {
                'symbol': symbol,
                'price': current_price,
                'change': current_price - previous_close,
                'return': daily_return,
                'volume': meta['regularMarketVolume'],
                'volatility': 0.02,  # Would need historical data for real volatility
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error parsing Yahoo data: {e}")
            return {}


class AlphaVantageAPI:
    """Alpha Vantage API integration"""
    
    def __init__(self, api_key: str = "demo"):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Get real-time data from Alpha Vantage"""
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_alpha_vantage_data(data, symbol)
            
        except Exception as e:
            print(f"Alpha Vantage API error: {e}")
        
        return None
    
    def _parse_alpha_vantage_data(self, data: Dict, symbol: str) -> Dict:
        """Parse Alpha Vantage response"""
        try:
            quote = data['Global Quote']
            
            price = float(quote['05. price'])
            change = float(quote['09. change'])
            change_percent = float(quote['10. change percent'].replace('%', ''))
            daily_return = change / (price - change)
            
            return {
                'symbol': symbol,
                'price': price,
                'change': change,
                'return': daily_return,
                'change_percent': change_percent,
                'volume': int(quote['06. volume']),
                'volatility': 0.02,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error parsing Alpha Vantage data: {e}")
            return {}


class MockDataProvider:
    """Mock data provider for testing and fallback"""
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Generate mock real-time data"""
        try:
            # Generate realistic mock data
            base_price = np.random.uniform(50, 500)
            change = np.random.normal(0, base_price * 0.02)
            daily_return = change / base_price
            
            return {
                'symbol': symbol,
                'price': base_price + change,
                'change': change,
                'return': daily_return,
                'volume': int(np.random.uniform(100000, 10000000)),
                'volatility': np.random.uniform(0.01, 0.04),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Mock data error: {e}")
            return None


class EconomicCalendarIntegration:
    """Integration with economic calendars for event-driven simulations"""
    
    def __init__(self):
        self.event_sources = [
            'federal_reserve',
            'economic_releases',
            'earnings_calendar',
            'geopolitical_events'
        ]
        self.events_cache = {}
    
    def get_upcoming_events(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get upcoming economic events that might impact simulations
        
        Parameters:
        days_ahead: Number of days to look ahead
        
        Returns:
        List of upcoming events
        """
        events = []
        
        for source in self.event_sources:
            try:
                source_events = self._fetch_events(source, days_ahead)
                events.extend(source_events)
            except Exception as e:
                print(f"⚠️ Error fetching {source} events: {e}")
        
        # Prioritize events by impact
        prioritized_events = self._prioritize_events(events)
        
        return prioritized_events
    
    def _fetch_events(self, source: str, days_ahead: int) -> List[Dict]:
        """Fetch events from a specific source"""
        # Mock implementation - would integrate with real APIs
        if source == 'federal_reserve':
            return [
                {
                    'date': datetime.now() + timedelta(days=7),
                    'type': 'fomc_meeting',
                    'title': 'FOMC Interest Rate Decision',
                    'impact': 'high',
                    'expected_impact': {'volatility': 1.5, 'correlation': 1.2}
                }
            ]
        elif source == 'economic_releases':
            return [
                {
                    'date': datetime.now() + timedelta(days=3),
                    'type': 'cpi_release',
                    'title': 'Consumer Price Index',
                    'impact': 'medium',
                    'expected_impact': {'volatility': 1.2, 'correlation': 1.1}
                }
            ]
        else:
            return []
    
    def _prioritize_events(self, events: List[Dict]) -> List[Dict]:
        """Prioritize events by impact and timing"""
        # Sort by date and impact
        impact_order = {'high': 3, 'medium': 2, 'low': 1}
        
        events.sort(key=lambda x: (
            x['date'],
            impact_order.get(x.get('impact', 'low'), 1)
        ))
        
        return events
    
    def adjust_for_events(self, base_parameters: Dict, events: List[Dict]) -> Dict:
        """
        Adjust simulation parameters for upcoming events
        
        Parameters:
        base_parameters: Base simulation parameters
        events: List of upcoming events
        
        Returns:
        Adjusted parameters
        """
        adjusted_params = base_parameters.copy()
        
        total_volatility_adjustment = 1.0
        total_correlation_adjustment = 1.0
        
        for event in events:
            if 'expected_impact' in event:
                impact = event['expected_impact']
                
                # Days until event
                days_until = (event['date'] - datetime.now()).days
                
                # Impact decay based on distance
                decay_factor = max(0, 1 - days_until / 30)
                
                if 'volatility' in impact:
                    total_volatility_adjustment *= (1 + (impact['volatility'] - 1) * decay_factor)
                
                if 'correlation' in impact:
                    total_correlation_adjustment *= (1 + (impact['correlation'] - 1) * decay_factor)
        
        # Apply adjustments
        if 'volatility_adjustment' in adjusted_params:
            adjusted_params['volatility_adjustment'] *= total_volatility_adjustment
        
        adjusted_params['correlation_multiplier'] = total_correlation_adjustment
        adjusted_params['upcoming_events'] = events
        
        return adjusted_params


class DynamicParameterUpdater:
    """Dynamic parameter updater based on real-time data and events"""
    
    def __init__(self):
        self.data_integration = RealTimeDataIntegration()
        self.calendar_integration = EconomicCalendarIntegration()
        self.update_history = []
    
    def update_parameters(self, symbols: List[str], base_parameters: Dict) -> Dict:
        """
        Update simulation parameters based on real-time data and events
        
        Parameters:
        symbols: List of symbols to monitor
        base_parameters: Base simulation parameters
        
        Returns:
        Updated parameters
        """
        print("🔄 Updating parameters with real-time data...")
        
        # Get real-time market data
        market_data = self.data_integration.fetch_real_time_data(symbols)
        market_adjustments = self.data_integration.update_simulation_parameters(market_data)
        
        # Get upcoming economic events
        upcoming_events = self.calendar_integration.get_upcoming_events()
        event_adjustments = self.calendar_integration.adjust_for_events(base_parameters, upcoming_events)
        
        # Combine adjustments
        updated_params = base_parameters.copy()
        
        # Apply market adjustments
        if 'return_adjustment' in market_adjustments:
            updated_params['equity_return'] = base_parameters.get('equity_return', 0.08) + market_adjustments['return_adjustment']
        
        if 'volatility_adjustment' in market_adjustments:
            updated_params['equity_volatility'] = base_parameters.get('equity_volatility', 0.16) * market_adjustments['volatility_adjustment']
        
        # Apply event adjustments
        if 'volatility_adjustment' in event_adjustments:
            updated_params['equity_volatility'] *= event_adjustments['volatility_adjustment']
        
        # Add metadata
        updated_params['update_timestamp'] = datetime.now().isoformat()
        updated_params['market_data'] = market_data
        updated_params['upcoming_events'] = upcoming_events
        updated_params['adjustments_applied'] = {
            'market_adjustments': market_adjustments,
            'event_adjustments': event_adjustments
        }
        
        # Store update history
        self.update_history.append({
            'timestamp': datetime.now().isoformat(),
            'parameters': updated_params.copy()
        })
        
        print(f"✅ Parameters updated successfully")
        print(f"   New equity return: {updated_params.get('equity_return', 'N/A'):.4f}")
        print(f"   New equity volatility: {updated_params.get('equity_volatility', 'N/A'):.4f}")
        print(f"   Upcoming events: {len(upcoming_events)}")
        
        return updated_params
    
    def get_update_history(self) -> List[Dict]:
        """Get history of parameter updates"""
        return self.update_history


# Example usage and demonstration
def demonstrate_real_time_integration():
    """Demonstrate real-time data integration"""
    print("📡 Real-Time Data Integration Demonstration")
    print("=" * 50)
    
    # Initialize components
    data_integration = RealTimeDataIntegration()
    calendar_integration = EconomicCalendarIntegration()
    parameter_updater = DynamicParameterUpdater()
    
    # Test symbols
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']
    
    print(f"\n📈 Fetching real-time data for {symbols}...")
    real_time_data = data_integration.fetch_real_time_data(symbols)
    
    for symbol, data in real_time_data.items():
        print(f"   {symbol}: ${data['price']:.2f} ({data['return']*100:+.2f}%)")
    
    print(f"\n📅 Getting upcoming economic events...")
    upcoming_events = calendar_integration.get_upcoming_events(days_ahead=30)
    
    for event in upcoming_events:
        print(f"   {event['date'].strftime('%Y-%m-%d')}: {event['title']} ({event['impact']})")
    
    print(f"\n⚙️ Updating simulation parameters...")
    base_parameters = {
        'equity_return': 0.08,
        'equity_volatility': 0.16,
        'bond_return': 0.04,
        'bond_volatility': 0.08,
        'equity_allocation': 0.70
    }
    
    updated_params = parameter_updater.update_parameters(symbols, base_parameters)
    
    print(f"\n📊 Parameter Updates Summary:")
    print(f"   Equity Return: {base_parameters['equity_return']:.4f} → {updated_params['equity_return']:.4f}")
    print(f"   Equity Volatility: {base_parameters['equity_volatility']:.4f} → {updated_params['equity_volatility']:.4f}")
    
    print(f"\n✨ Real-time integration demonstration complete!")
    
    return updated_params, real_time_data, upcoming_events


if __name__ == "__main__":
    # Run demonstration
    demonstrate_real_time_integration()
