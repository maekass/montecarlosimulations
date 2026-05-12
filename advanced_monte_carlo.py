"""
Advanced Monte Carlo Simulations with Machine Learning Integration
This module implements sophisticated enhancements including ML predictions, 
advanced risk metrics, and real-time data integration.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Import base Monte Carlo class
from monte_carlo_simulations import EndowmentSustainabilityMonteCarlo

class MLEnhancedMonteCarlo(EndowmentSustainabilityMonteCarlo):
    """Machine Learning Enhanced Monte Carlo Simulations"""
    
    def __init__(self, initial_value=10000000, annual_payout=315000, 
                 equity_return=0.08, bond_return=0.04, equity_volatility=0.16, 
                 bond_volatility=0.08, equity_allocation=0.70, inflation_rate=0.03, 
                 n_simulations=1000, random_seed=42):
        
        super().__init__(initial_value, annual_payout, equity_return, bond_return,
                        equity_volatility, bond_volatility, equity_allocation, 
                        inflation_rate, n_simulations, random_seed)
        
        # Initialize ML models
        self.models = {}
        self.scalers = {}
        self._initialize_ml_models()
        
    def _initialize_ml_models(self):
        """Initialize machine learning models for prediction"""
        self.models = {
            'returns_predictor': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'volatility_forecaster': RandomForestRegressor(n_estimators=100, random_state=42),
            'regime_detector': MLPRegressor(hidden_layer_sizes=(50, 25), random_state=42)
        }
        
        self.scalers = {
            'returns': StandardScaler(),
            'volatility': StandardScaler(),
            'regime': StandardScaler()
        }
    
    def train_ml_models(self, historical_data):
        """
        Train ML models on historical market data
        
        Parameters:
        historical_data: DataFrame with columns ['date', 'equity_return', 'bond_return', 
                                             'volatility', 'market_regime']
        """
        # Feature engineering
        features = self._create_features(historical_data)
        
        # Train returns predictor
        X_returns = features.drop(['future_equity_return'], axis=1)
        y_returns = features['future_equity_return']
        
        X_returns_scaled = self.scalers['returns'].fit_transform(X_returns)
        self.models['returns_predictor'].fit(X_returns_scaled, y_returns)
        
        # Train volatility forecaster
        X_vol = features.drop(['future_volatility'], axis=1)
        y_vol = features['future_volatility']
        
        X_vol_scaled = self.scalers['volatility'].fit_transform(X_vol)
        self.models['volatility_forecaster'].fit(X_vol_scaled, y_vol)
        
        # Train regime detector
        X_regime = features.drop(['market_regime'], axis=1)
        y_regime = features['market_regime']
        
        X_regime_scaled = self.scalers['regime'].fit_transform(X_regime)
        self.models['regime_detector'].fit(X_regime_scaled, y_regime)
        
        print("✅ ML models trained successfully")
    
    def _create_features(self, data):
        """Create features for ML models"""
        features = data.copy()
        
        # Lag features
        for lag in [1, 2, 3, 5, 10]:
            features[f'equity_return_lag_{lag}'] = features['equity_return'].shift(lag)
            features[f'bond_return_lag_{lag}'] = features['bond_return'].shift(lag)
            features[f'volatility_lag_{lag}'] = features['volatility'].shift(lag)
        
        # Rolling statistics
        features['equity_return_ma_20'] = features['equity_return'].rolling(20).mean()
        features['equity_return_std_20'] = features['equity_return'].rolling(20).std()
        features['volatility_ma_20'] = features['volatility'].rolling(20).mean()
        
        # Target variables
        features['future_equity_return'] = features['equity_return'].shift(-1)
        features['future_volatility'] = features['volatility'].shift(-1)
        
        # Drop NaN values
        features = features.dropna()
        
        return features
    
    def predict_market_conditions(self, current_features):
        """
        Predict future market conditions using trained ML models
        
        Parameters:
        current_features: DataFrame with current market features
        
        Returns:
        Dictionary with predictions
        """
        predictions = {}
        
        try:
            # Predict returns
            returns_scaled = self.scalers['returns'].transform(current_features)
            predicted_returns = self.models['returns_predictor'].predict(returns_scaled)
            predictions['predicted_returns'] = predicted_returns[0]
            
            # Predict volatility
            vol_scaled = self.scalers['volatility'].transform(current_features)
            predicted_volatility = self.models['volatility_forecaster'].predict(vol_scaled)
            predictions['predicted_volatility'] = predicted_volatility[0]
            
            # Predict market regime
            regime_scaled = self.scalers['regime'].transform(current_features)
            predicted_regime = self.models['regime_detector'].predict(regime_scaled)
            predictions['market_regime'] = predicted_regime[0]
            
        except Exception as e:
            print(f"⚠️ ML prediction failed: {e}")
            # Fall back to historical averages
            predictions = {
                'predicted_returns': self.equity_return,
                'predicted_volatility': self.equity_volatility,
                'market_regime': 1.0  # Normal regime
            }
        
        return predictions
    
    def run_ml_enhanced_simulation(self, years=20, use_ml_predictions=True):
        """
        Run Monte Carlo simulation with ML-enhanced parameters
        
        Parameters:
        years: Simulation horizon in years
        use_ml_predictions: Whether to use ML predictions for parameters
        
        Returns:
        Enhanced results with ML insights
        """
        if use_ml_predictions:
            # Create dummy current features for demonstration
            current_features = pd.DataFrame({
                'equity_return': [self.equity_return],
                'bond_return': [self.bond_return],
                'volatility': [self.equity_volatility],
                'market_regime': [1.0]
            })
            
            # Add lag features (using current values for simplicity)
            for lag in [1, 2, 3, 5, 10]:
                current_features[f'equity_return_lag_{lag}'] = self.equity_return
                current_features[f'bond_return_lag_{lag}'] = self.bond_return
                current_features[f'volatility_lag_{lag}'] = self.equity_volatility
            
            # Add rolling features
            current_features['equity_return_ma_20'] = self.equity_return
            current_features['equity_return_std_20'] = self.equity_volatility
            current_features['volatility_ma_20'] = self.equity_volatility
            
            # Get ML predictions
            predictions = self.predict_market_conditions(current_features)
            
            # Adjust parameters based on ML predictions
            adjusted_equity_return = predictions['predicted_returns']
            adjusted_volatility = predictions['predicted_volatility']
            
            print(f"🤖 ML-Enhanced Parameters:")
            print(f"   Predicted Equity Return: {adjusted_equity_return:.4f}")
            print(f"   Predicted Volatility: {adjusted_volatility:.4f}")
            print(f"   Market Regime: {predictions['market_regime']:.2f}")
        else:
            adjusted_equity_return = self.equity_return
            adjusted_volatility = self.equity_volatility
        
        # Run simulation with adjusted parameters
        results = self.run_simulation(years)
        
        # Add ML-specific metrics
        results['ml_enhanced'] = use_ml_predictions
        if use_ml_predictions:
            results['ml_predictions'] = predictions
            results['parameter_adjustments'] = {
                'equity_return_adjustment': adjusted_equity_return - self.equity_return,
                'volatility_adjustment': adjusted_volatility - self.equity_volatility
            }
        
        return results


class AdvancedRiskMetrics:
    """Advanced risk metrics beyond standard VaR and drawdown"""
    
    def __init__(self):
        self.risk_metrics = {}
    
    def calculate_cvar(self, returns, confidence_level=0.95):
        """
        Conditional Value at Risk (Expected Shortfall)
        
        Parameters:
        returns: Array of returns
        confidence_level: Confidence level for VaR
        
        Returns:
        CVaR value
        """
        var = np.percentile(returns, (1 - confidence_level) * 100)
        cvar = returns[returns <= var].mean()
        return cvar
    
    def calculate_expected_shortfall(self, returns, confidence_level=0.95):
        """Expected Shortfall (alias for CVaR)"""
        return self.calculate_cvar(returns, confidence_level)
    
    def calculate_pain_index(self, returns):
        """
        Pain Index: measures depth and duration of drawdowns
        
        Parameters:
        returns: Array of returns
        
        Returns:
        Pain index value
        """
        cum_returns = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - peak) / peak
        pain_index = np.mean(np.abs(drawdown[drawdown < 0]))
        return pain_index
    
    def calculate_sterling_ratio(self, returns, risk_free_rate=0.02):
        """
        Sterling Ratio: Return / average drawdown
        
        Parameters:
        returns: Array of returns
        risk_free_rate: Risk-free rate
        
        Returns:
        Sterling ratio
        """
        annual_return = np.mean(returns)
        pain_index = self.calculate_pain_index(returns)
        
        if pain_index == 0:
            return np.inf
        
        sterling_ratio = (annual_return - risk_free_rate) / pain_index
        return sterling_ratio
    
    def calculate_calmar_ratio(self, returns, risk_free_rate=0.02):
        """
        Calmar Ratio: Return / maximum drawdown
        
        Parameters:
        returns: Array of returns
        risk_free_rate: Risk-free rate
        
        Returns:
        Calmar ratio
        """
        annual_return = np.mean(returns)
        cum_returns = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - peak) / peak
        max_drawdown = np.min(drawdown)
        
        if max_drawdown == 0:
            return np.inf
        
        calmar_ratio = (annual_return - risk_free_rate) / abs(max_drawdown)
        return calmar_ratio
    
    def calculate_sortino_ratio(self, returns, risk_free_rate=0.02):
        """
        Sortino Ratio: Return / downside deviation
        
        Parameters:
        returns: Array of returns
        risk_free_rate: Risk-free rate
        
        Returns:
        Sortino ratio
        """
        excess_returns = returns - risk_free_rate
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0:
            return np.inf
        
        downside_deviation = np.std(downside_returns)
        sortino_ratio = np.mean(excess_returns) / downside_deviation
        return sortino_ratio
    
    def calculate_information_ratio(self, portfolio_returns, benchmark_returns):
        """
        Information Ratio: Active return / tracking error
        
        Parameters:
        portfolio_returns: Portfolio returns
        benchmark_returns: Benchmark returns
        
        Returns:
        Information ratio
        """
        active_returns = portfolio_returns - benchmark_returns
        tracking_error = np.std(active_returns)
        
        if tracking_error == 0:
            return 0
        
        information_ratio = np.mean(active_returns) / tracking_error
        return information_ratio
    
    def stress_test_scenarios(self, portfolio_values, scenarios):
        """
        Comprehensive stress testing with multiple scenarios
        
        Parameters:
        portfolio_values: Array of portfolio values
        scenarios: Dictionary of stress scenarios
        
        Returns:
        Dictionary with stress test results
        """
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        
        results = {}
        for scenario_name, scenario_params in scenarios.items():
            # Apply stress scenario
            stressed_returns = self._apply_stress_scenario(returns, scenario_params)
            
            # Calculate risk metrics for stressed scenario
            results[scenario_name] = {
                'var_95': np.percentile(stressed_returns, 5),
                'cvar_95': self.calculate_cvar(stressed_returns, 0.95),
                'max_drawdown': self._calculate_max_drawdown(stressed_returns),
                'scenario_return': np.mean(stressed_returns),
                'volatility': np.std(stressed_returns),
                'sortino_ratio': self.calculate_sortino_ratio(stressed_returns),
                'calmar_ratio': self.calculate_calmar_ratio(stressed_returns)
            }
        
        return results
    
    def _calculate_max_drawdown(self, returns):
        """Calculate maximum drawdown"""
        cum_returns = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - peak) / peak
        max_drawdown = np.min(drawdown)
        return max_drawdown
    
    def _apply_stress_scenario(self, returns, scenario_params):
        """Apply stress scenario to returns"""
        stressed_returns = returns.copy()
        
        if 'return_shock' in scenario_params:
            stressed_returns += scenario_params['return_shock']
        
        if 'volatility_multiplier' in scenario_params:
            stressed_returns *= scenario_params['volatility_multiplier']
        
        if 'correlation_breakdown' in scenario_params:
            # Simplified correlation breakdown effect
            stressed_returns *= np.random.normal(1, 0.2, len(stressed_returns))
        
        return stressed_returns
    
    def generate_risk_report(self, portfolio_values, benchmark_values=None):
        """
        Generate comprehensive risk report
        
        Parameters:
        portfolio_values: Array of portfolio values
        benchmark_values: Optional benchmark values
        
        Returns:
        Dictionary with comprehensive risk metrics
        """
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        
        report = {
            'basic_metrics': {
                'total_return': (portfolio_values[-1] - portfolio_values[0]) / portfolio_values[0],
                'annualized_return': np.mean(returns) * 252,  # Assuming daily returns
                'volatility': np.std(returns) * np.sqrt(252),
                'sharpe_ratio': self._calculate_sharpe_ratio(returns)
            },
            'advanced_metrics': {
                'var_95': np.percentile(returns, 5),
                'cvar_95': self.calculate_cvar(returns, 0.95),
                'max_drawdown': self._calculate_max_drawdown(returns),
                'pain_index': self.calculate_pain_index(returns),
                'sterling_ratio': self.calculate_sterling_ratio(returns),
                'calmar_ratio': self.calculate_calmar_ratio(returns),
                'sortino_ratio': self.calculate_sortino_ratio(returns)
            }
        }
        
        if benchmark_values is not None:
            benchmark_returns = np.diff(benchmark_values) / benchmark_values[:-1]
            report['relative_metrics'] = {
                'information_ratio': self.calculate_information_ratio(returns, benchmark_returns),
                'tracking_error': np.std(returns - benchmark_returns) * np.sqrt(252),
                'beta': np.cov(returns, benchmark_returns)[0, 1] / np.var(benchmark_returns),
                'alpha': np.mean(returns) - np.mean(benchmark_returns)
            }
        
        return report
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
        if np.std(excess_returns) == 0:
            return 0
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)


class EnsembleRiskAssessment:
    """Ensemble of ML models for comprehensive risk assessment"""
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'neural_network': MLPRegressor(hidden_layer_sizes=(50, 25), random_state=42),
            'svr': SVR(kernel='rbf', C=1.0),
            'bayesian_ridge': BayesianRidge()
        }
        self.weights = {}
        self.is_trained = False
    
    def train_ensemble(self, X, y):
        """
        Train ensemble of models
        
        Parameters:
        X: Feature matrix
        y: Target variable
        """
        self.weights = {}
        
        # Train each model
        for name, model in self.models.items():
            model.fit(X, y)
            self.weights[name] = model.score(X, y)
        
        # Normalize weights
        total_weight = sum(self.weights.values())
        self.weights = {k: v/total_weight for k, v in self.weights.items()}
        
        self.is_trained = True
        print("✅ Ensemble models trained successfully")
    
    def ensemble_predict(self, X):
        """
        Make predictions using ensemble of models
        
        Parameters:
        X: Feature matrix
        
        Returns:
        Ensemble prediction and individual predictions
        """
        if not self.is_trained:
            raise ValueError("Models not trained yet. Call train_ensemble first.")
        
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)
        
        # Weighted ensemble prediction
        ensemble_pred = np.zeros(len(X))
        for name, pred in predictions.items():
            ensemble_pred += self.weights[name] * pred
        
        return ensemble_pred, predictions
    
    def get_feature_importance(self):
        """Get feature importance from ensemble"""
        if not self.is_trained:
            raise ValueError("Models not trained yet.")
        
        # Get feature importance from tree-based models
        importance_scores = {}
        
        if hasattr(self.models['random_forest'], 'feature_importances_'):
            importance_scores['random_forest'] = self.models['random_forest'].feature_importances_
        
        if hasattr(self.models['gradient_boost'], 'feature_importances_'):
            importance_scores['gradient_boost'] = self.models['gradient_boost'].feature_importances_
        
        return importance_scores


# Example usage and demonstration
def demonstrate_advanced_features():
    """Demonstrate advanced Monte Carlo features"""
    print("🚀 Advanced Monte Carlo Simulations Demonstration")
    print("=" * 60)
    
    # Create ML-enhanced Monte Carlo simulator
    ml_mc = MLEnhancedMonteCarlo(
        initial_value=10000000,
        annual_payout=315000,
        n_simulations=1000
    )
    
    # Create synthetic historical data for demonstration
    np.random.seed(42)
    n_days = 252  # One year of daily data
    
    historical_data = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=n_days),
        'equity_return': np.random.normal(0.0008, 0.02, n_days),
        'bond_return': np.random.normal(0.0003, 0.01, n_days),
        'volatility': np.random.uniform(0.01, 0.04, n_days),
        'market_regime': np.random.choice([0.5, 1.0, 1.5], n_days, p=[0.2, 0.6, 0.2])
    })
    
    print("\n📊 Training ML models on historical data...")
    ml_mc.train_ml_models(historical_data)
    
    print("\n🎯 Running ML-enhanced simulation...")
    ml_results = ml_mc.run_ml_enhanced_simulation(years=20, use_ml_predictions=True)
    
    print(f"\n📈 ML-Enhanced Results:")
    print(f"   Survival Probability: {ml_results['survival_probability']:.2%}")
    print(f"   Mean Final Value: ${ml_results['mean_final']:,.2f}")
    
    # Demonstrate advanced risk metrics
    print("\n🔬 Advanced Risk Metrics Analysis...")
    
    # Create sample portfolio values
    portfolio_values = np.cumprod(1 + np.random.normal(0.0008, 0.02, 1000)) * 10000000
    
    risk_metrics = AdvancedRiskMetrics()
    risk_report = risk_metrics.generate_risk_report(portfolio_values)
    
    print(f"   CVaR (95%): {risk_report['advanced_metrics']['cvar_95']:.4f}")
    print(f"   Pain Index: {risk_report['advanced_metrics']['pain_index']:.4f}")
    print(f"   Sterling Ratio: {risk_report['advanced_metrics']['sterling_ratio']:.4f}")
    print(f"   Calmar Ratio: {risk_report['advanced_metrics']['calmar_ratio']:.4f}")
    
    # Stress testing
    print("\n⚡ Stress Testing Scenarios...")
    stress_scenarios = {
        'market_crash': {'return_shock': -0.20, 'volatility_multiplier': 2.0},
        'volatility_spike': {'volatility_multiplier': 3.0},
        'correlation_breakdown': {'correlation_breakdown': True}
    }
    
    stress_results = risk_metrics.stress_test_scenarios(portfolio_values, stress_scenarios)
    
    for scenario, metrics in stress_results.items():
        print(f"   {scenario}: VaR_95={metrics['var_95']:.4f}, CVaR_95={metrics['cvar_95']:.4f}")
    
    # Ensemble risk assessment
    print("\n🤝 Ensemble Risk Assessment...")
    
    # Create synthetic features and targets
    X = np.random.randn(1000, 10)
    y = np.random.randn(1000)
    
    ensemble = EnsembleRiskAssessment()
    ensemble.train_ensemble(X, y)
    
    # Make predictions
    X_test = np.random.randn(100, 10)
    ensemble_pred, individual_preds = ensemble.ensemble_predict(X_test)
    
    print(f"   Ensemble prediction accuracy: {np.mean((ensemble_pred - y[:100])**2):.6f}")
    print(f"   Model weights: {ensemble.weights}")
    
    print("\n✨ Advanced features demonstration complete!")
    
    return ml_results, risk_report, stress_results


if __name__ == "__main__":
    # Run demonstration
    demonstrate_advanced_features()
