"""
Monte Carlo Simulations Portfolio
A collection of Monte Carlo simulation examples for finance, risk, pricing, and optimization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class MonteCarloSimulator:
    """Base class for Monte Carlo simulations"""
    
    def __init__(self, n_simulations=10000, random_seed=42):
        self.n_simulations = n_simulations
        np.random.seed(random_seed)
        
    def run_simulation(self):
        raise NotImplementedError("Subclasses must implement run_simulation")

class PortfolioMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for portfolio returns"""
    
    def __init__(self, returns, volatility, initial_investment, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.returns = returns
        self.volatility = volatility
        self.initial_investment = initial_investment
        
    def simulate_returns(self, time_horizon=252):
        """
        Simulate portfolio returns using Geometric Brownian Motion
        time_horizon: number of trading days (default: 252 = 1 year)
        """
        dt = 1 / time_horizon
        daily_returns = (self.returns - 0.5 * self.volatility**2) * dt + \
                       self.volatility * np.sqrt(dt) * np.random.normal(0, 1, (self.n_simulations, time_horizon))
        
        cumulative_returns = np.cumprod(1 + daily_returns, axis=1)
        portfolio_values = self.initial_investment * cumulative_returns
        
        return portfolio_values
    
    def run_simulation(self, time_horizon=252):
        """Run portfolio simulation and return statistics"""
        portfolio_values = self.simulate_returns(time_horizon)
        final_values = portfolio_values[:, -1]
        
        return {
            'final_values': final_values,
            'mean': np.mean(final_values),
            'median': np.median(final_values),
            'std': np.std(final_values),
            'percentile_5': np.percentile(final_values, 5),
            'percentile_95': np.percentile(final_values, 95),
            'probability_profit': np.mean(final_values > self.initial_investment),
            'all_paths': portfolio_values
        }

class OptionPricingMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for European option pricing"""
    
    def __init__(self, S, K, T, r, sigma, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.S = S  # Current stock price
        self.K = K  # Strike price
        self.T = T  # Time to maturity (years)
        self.r = r  # Risk-free rate
        self.sigma = sigma  # Volatility
        
    def simulate_stock_price(self, n_steps=252):
        """Simulate stock price paths using Geometric Brownian Motion"""
        dt = self.T / n_steps
        paths = np.zeros((self.n_simulations, n_steps + 1))
        paths[:, 0] = self.S
        
        for t in range(1, n_steps + 1):
            z = np.random.standard_normal(self.n_simulations)
            paths[:, t] = paths[:, t-1] * np.exp((self.r - 0.5 * self.sigma**2) * dt + 
                                                  self.sigma * np.sqrt(dt) * z)
        
        return paths
    
    def price_call_option(self, n_steps=252):
        """Price European call option using Monte Carlo"""
        paths = self.simulate_stock_price(n_steps)
        final_prices = paths[:, -1]
        payoffs = np.maximum(final_prices - self.K, 0)
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        
        return {
            'option_price': option_price,
            'std_error': np.std(np.exp(-self.r * self.T) * payoffs) / np.sqrt(self.n_simulations),
            'paths': paths
        }
    
    def price_put_option(self, n_steps=252):
        """Price European put option using Monte Carlo"""
        paths = self.simulate_stock_price(n_steps)
        final_prices = paths[:, -1]
        payoffs = np.maximum(self.K - final_prices, 0)
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        
        return {
            'option_price': option_price,
            'std_error': np.std(np.exp(-self.r * self.T) * payoffs) / np.sqrt(self.n_simulations),
            'paths': paths
        }
    
    def run_simulation(self, option_type='call', n_steps=252):
        """Run option pricing simulation"""
        if option_type == 'call':
            return self.price_call_option(n_steps)
        else:
            return self.price_put_option(n_steps)

class RiskVaRMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for Value at Risk (VaR) calculation"""
    
    def __init__(self, portfolio_value, returns, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.portfolio_value = portfolio_value
        self.returns = returns
        
    def simulate_portfolio_value(self, confidence_level=0.95):
        """Calculate VaR using Monte Carlo simulation"""
        simulated_returns = np.random.choice(self.returns, size=self.n_simulations, replace=True)
        simulated_values = self.portfolio_value * (1 + simulated_returns)
        
        # Calculate VaR
        var = np.percentile(simulated_values, 100 - confidence_level * 100)
        var_dollar = self.portfolio_value - var
        
        # Calculate Expected Shortfall (CVaR)
        cvar = np.mean(simulated_values[simulated_values <= var])
        cvar_dollar = self.portfolio_value - cvar
        
        return {
            'var': var,
            'var_dollar': var_dollar,
            'cvar': cvar,
            'cvar_dollar': cvar_dollar,
            'confidence_level': confidence_level,
            'simulated_values': simulated_values
        }
    
    def run_simulation(self, confidence_level=0.95):
        """Run VaR simulation"""
        return self.simulate_portfolio_value(confidence_level)

class ProjectCostMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for project cost estimation"""
    
    def __init__(self, base_cost, cost_variations, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.base_cost = base_cost
        self.cost_variations = cost_variations  # dict of {component: (min, max, distribution)}
        
    def simulate_total_cost(self):
        """Simulate total project cost using specified distributions"""
        total_costs = np.zeros(self.n_simulations)
        
        for component, (min_val, max_val, dist_type) in self.cost_variations.items():
            if dist_type == 'uniform':
                component_cost = np.random.uniform(min_val, max_val, self.n_simulations)
            elif dist_type == 'triangular':
                mode_val = (min_val + max_val) / 2
                component_cost = np.random.triangular(min_val, mode_val, max_val, self.n_simulations)
            elif dist_type == 'normal':
                mean_val = (min_val + max_val) / 2
                std_val = (max_val - min_val) / 6
                component_cost = np.random.normal(mean_val, std_val, self.n_simulations)
                component_cost = np.clip(component_cost, min_val, max_val)
            
            total_costs += component_cost
        
        return total_costs
    
    def run_simulation(self):
        """Run project cost simulation"""
        total_costs = self.simulate_total_cost()
        
        return {
            'total_costs': total_costs,
            'mean': np.mean(total_costs),
            'median': np.median(total_costs),
            'std': np.std(total_costs),
            'percentile_10': np.percentile(total_costs, 10),
            'percentile_90': np.percentile(total_costs, 90),
            'percentile_95': np.percentile(total_costs, 95)
        }

class RevenueForecastMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for revenue forecasting"""
    
    def __init__(self, base_revenue, growth_rate, volatility, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.base_revenue = base_revenue
        self.growth_rate = growth_rate
        self.volatility = volatility
        
    def simulate_revenue(self, years=5):
        """Simulate revenue over multiple years"""
        revenues = np.zeros((self.n_simulations, years))
        revenues[:, 0] = self.base_revenue
        
        for year in range(1, years):
            growth = np.random.normal(self.growth_rate, self.volatility, self.n_simulations)
            revenues[:, year] = revenues[:, year-1] * (1 + growth)
        
        return revenues
    
    def run_simulation(self, years=5):
        """Run revenue forecast simulation"""
        revenues = self.simulate_revenue(years)
        final_revenues = revenues[:, -1]
        
        return {
            'revenues': revenues,
            'final_revenues': final_revenues,
            'mean_final': np.mean(final_revenues),
            'median_final': np.median(final_revenues),
            'std_final': np.std(final_revenues),
            'percentile_10': np.percentile(final_revenues, 10),
            'percentile_90': np.percentile(final_revenues, 90)
        }

# Non-Profit Endowment Simulations

class EndowmentSustainabilityMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for non-profit endowment sustainability planning"""
    
    def __init__(self, initial_value, annual_payout, equity_return, bond_return, equity_volatility, 
                 bond_volatility, equity_allocation, inflation_rate, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.annual_payout = annual_payout
        self.equity_return = equity_return
        self.bond_return = bond_return
        self.equity_volatility = equity_volatility
        self.bond_volatility = bond_volatility
        self.equity_allocation = equity_allocation
        self.bond_allocation = 1 - equity_allocation
        self.inflation_rate = inflation_rate
        
    def simulate_endowment(self, years=20):
        """
        Simulate endowment sustainability over time horizon
        Tests whether portfolio can support planned annual payouts without depleting principal
        """
        endowment_values = np.zeros((self.n_simulations, years + 1))
        endowment_values[:, 0] = self.initial_value
        
        for year in range(years):
            # Simulate returns for each asset class
            equity_returns = np.random.normal(self.equity_return, self.equity_volatility, self.n_simulations)
            bond_returns = np.random.normal(self.bond_return, self.bond_volatility, self.n_simulations)
            
            # Portfolio return
            portfolio_return = (self.equity_allocation * equity_returns + 
                               self.bond_allocation * bond_returns)
            
            # Apply return before payout
            endowment_values[:, year + 1] = endowment_values[:, year] * (1 + portfolio_return)
            
            # Apply payout (inflation-adjusted)
            inflation_adjusted_payout = self.annual_payout * (1 + self.inflation_rate) ** year
            endowment_values[:, year + 1] -= inflation_adjusted_payout
            
            # Ensure no negative values
            endowment_values[:, year + 1] = np.maximum(endowment_values[:, year + 1], 0)
        
        return endowment_values
    
    def run_simulation(self, years=20):
        """Run endowment sustainability simulation"""
        endowment_values = self.simulate_endowment(years)
        final_values = endowment_values[:, -1]
        
        # Calculate probability of survival (maintaining purchasing power)
        purchasing_power_threshold = self.initial_value * 0.8  # 80% of initial value
        survival_probability = np.mean(final_values >= purchasing_power_threshold)
        
        return {
            'endowment_values': endowment_values,
            'final_values': final_values,
            'mean_final': np.mean(final_values),
            'median_final': np.median(final_values),
            'std_final': np.std(final_values),
            'survival_probability': survival_probability,
            'purchasing_power_threshold': purchasing_power_threshold
        }

class WithdrawalStrategyMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for comparing withdrawal strategies"""
    
    def __init__(self, initial_value, returns, volatility, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.returns = returns
        self.volatility = volatility
        
    def simulate_fixed_withdrawal(self, withdrawal_amount, years=20):
        """Simulate fixed-dollar withdrawal strategy"""
        portfolio_values = np.zeros((self.n_simulations, years + 1))
        portfolio_values[:, 0] = self.initial_value
        
        for year in range(years):
            portfolio_return = np.random.normal(self.returns, self.volatility, self.n_simulations)
            portfolio_values[:, year + 1] = portfolio_values[:, year] * (1 + portfolio_return) - withdrawal_amount
            portfolio_values[:, year + 1] = np.maximum(portfolio_values[:, year + 1], 0)
        
        return portfolio_values
    
    def simulate_percentage_withdrawal(self, withdrawal_rate, years=20):
        """Simulate percentage-based withdrawal strategy"""
        portfolio_values = np.zeros((self.n_simulations, years + 1))
        portfolio_values[:, 0] = self.initial_value
        
        for year in range(years):
            portfolio_return = np.random.normal(self.returns, self.volatility, self.n_simulations)
            withdrawal_amount = portfolio_values[:, year] * withdrawal_rate
            portfolio_values[:, year + 1] = portfolio_values[:, year] * (1 + portfolio_return) - withdrawal_amount
            portfolio_values[:, year + 1] = np.maximum(portfolio_values[:, year + 1], 0)
        
        return portfolio_values
    
    def compare_strategies(self, fixed_amount, percentage_rate, years=20):
        """Compare fixed-dollar vs percentage-based withdrawal strategies"""
        fixed_values = self.simulate_fixed_withdrawal(fixed_amount, years)
        percentage_values = self.simulate_percentage_withdrawal(percentage_rate, years)
        
        fixed_survival = np.mean(fixed_values[:, -1] > 0)
        percentage_survival = np.mean(percentage_values[:, -1] > 0)
        
        return {
            'fixed_values': fixed_values,
            'percentage_values': percentage_values,
            'fixed_survival_rate': fixed_survival,
            'percentage_survival_rate': percentage_survival,
            'fixed_mean_final': np.mean(fixed_values[:, -1]),
            'percentage_mean_final': np.mean(percentage_values[:, -1])
        }
    
    def run_simulation(self, fixed_amount, percentage_rate, years=20):
        """Run withdrawal strategy comparison"""
        return self.compare_strategies(fixed_amount, percentage_rate, years)

class AssetAllocationMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation for testing different asset allocations"""
    
    def __init__(self, initial_value, allocations, returns_dict, volatility_dict, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.allocations = allocations  # dict of {allocation_name: {equity: %, bond: %}}
        self.returns_dict = returns_dict  # dict of {equity: return, bond: return}
        self.volatility_dict = volatility_dict  # dict of {equity: vol, bond: vol}
        
    def simulate_allocation(self, equity_allocation, years=20):
        """Simulate portfolio with specific equity allocation"""
        bond_allocation = 1 - equity_allocation
        portfolio_values = np.zeros((self.n_simulations, years + 1))
        portfolio_values[:, 0] = self.initial_value
        
        equity_return = self.returns_dict['equity']
        bond_return = self.returns_dict['bond']
        equity_vol = self.volatility_dict['equity']
        bond_vol = self.volatility_dict['bond']
        
        for year in range(years):
            equity_returns = np.random.normal(equity_return, equity_vol, self.n_simulations)
            bond_returns = np.random.normal(bond_return, bond_vol, self.n_simulations)
            
            portfolio_return = (equity_allocation * equity_returns + bond_allocation * bond_returns)
            portfolio_values[:, year + 1] = portfolio_values[:, year] * (1 + portfolio_return)
        
        return portfolio_values
    
    def compare_allocations(self, years=20):
        """Compare different asset allocation strategies"""
        results = {}
        
        for alloc_name, allocation in self.allocations.items():
            equity_alloc = allocation['equity']
            portfolio_values = self.simulate_allocation(equity_alloc, years)
            
            results[alloc_name] = {
                'values': portfolio_values,
                'mean_final': np.mean(portfolio_values[:, -1]),
                'median_final': np.median(portfolio_values[:, -1]),
                'std_final': np.std(portfolio_values[:, -1]),
                'percentile_5': np.percentile(portfolio_values[:, -1], 5),
                'percentile_95': np.percentile(portfolio_values[:, -1], 95)
            }
        
        return results
    
    def run_simulation(self, years=20):
        """Run asset allocation comparison"""
        return self.compare_allocations(years)

# Advanced Statistical Methods and ML Integration for Non-Profit Endowments

class BayesianEndowmentMonteCarlo(MonteCarloSimulator):
    """Bayesian Monte Carlo simulation with prior distributions and posterior inference"""
    
    def __init__(self, initial_value, annual_payout, prior_returns, prior_volatility, 
                 n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.annual_payout = annual_payout
        self.prior_returns = prior_returns  # dict with mean and std
        self.prior_volatility = prior_volatility  # dict with mean and std
        
    def sample_from_priors(self):
        """Sample parameters from prior distributions"""
        equity_return = np.random.normal(self.prior_returns['equity']['mean'], 
                                        self.prior_returns['equity']['std'], self.n_simulations)
        bond_return = np.random.normal(self.prior_returns['bond']['mean'], 
                                      self.prior_returns['bond']['std'], self.n_simulations)
        equity_vol = np.random.gamma(2, self.prior_volatility['equity']['std'], self.n_simulations)
        bond_vol = np.random.gamma(2, self.prior_volatility['bond']['std'], self.n_simulations)
        
        return equity_return, bond_return, equity_vol, bond_vol
    
    def simulate_bayesian_endowment(self, years=20):
        """
        Bayesian simulation: sample parameters from priors, then simulate endowment
        Returns posterior distribution of outcomes
        """
        equity_return, bond_return, equity_vol, bond_vol = self.sample_from_priors()
        
        endowment_values = np.zeros((self.n_simulations, years + 1))
        endowment_values[:, 0] = self.initial_value
        
        for year in range(years):
            for i in range(self.n_simulations):
                portfolio_return = (0.7 * np.random.normal(equity_return[i], equity_vol[i]) + 
                                   0.3 * np.random.normal(bond_return[i], bond_vol[i]))
                endowment_values[i, year + 1] = endowment_values[i, year] * (1 + portfolio_return) - self.annual_payout
                endowment_values[i, year + 1] = max(endowment_values[i, year + 1], 0)
        
        return endowment_values
    
    def run_simulation(self, years=20):
        """Run Bayesian simulation with posterior inference"""
        endowment_values = self.simulate_bayesian_endowment(years)
        final_values = endowment_values[:, -1]
        
        return {
            'endowment_values': endowment_values,
            'final_values': final_values,
            'posterior_mean': np.mean(final_values),
            'posterior_std': np.std(final_values),
            'credible_interval_95': np.percentile(final_values, [2.5, 97.5]),
            'credible_interval_50': np.percentile(final_values, [25, 75])
        }

class LatinHypercubeSamplingMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation using Latin Hypercube Sampling for efficiency"""
    
    def __init__(self, initial_value, returns, volatility, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.returns = returns
        self.volatility = volatility
        
    def generate_lhs_samples(self, n_samples, n_dimensions):
        """Generate Latin Hypercube Samples"""
        from scipy.stats import qmc
        
        sampler = qmc.LatinHypercube(d=n_dimensions)
        samples = sampler.random(n=n_samples)
        return samples
    
    def simulate_lhs_portfolio(self, time_horizon=252):
        """Simulate portfolio using Latin Hypercube Sampling for more efficient sampling"""
        # Generate LHS samples for return and volatility
        lhs_samples = self.generate_lhs_samples(self.n_simulations, 2)
        
        # Transform samples to parameter space
        sampled_returns = self.returns + (lhs_samples[:, 0] - 0.5) * self.returns * 0.5
        sampled_volatility = self.volatility + (lhs_samples[:, 1] - 0.5) * self.volatility * 0.5
        
        dt = 1 / time_horizon
        portfolio_values = np.zeros((self.n_simulations, time_horizon + 1))
        portfolio_values[:, 0] = self.initial_value
        
        for t in range(time_horizon):
            for i in range(self.n_simulations):
                z = np.random.standard_normal()
                portfolio_return = (sampled_returns[i] - 0.5 * sampled_volatility[i]**2) * dt + \
                                   sampled_volatility[i] * np.sqrt(dt) * z
                portfolio_values[i, t + 1] = portfolio_values[i, t] * (1 + portfolio_return)
        
        return portfolio_values
    
    def run_simulation(self, time_horizon=252):
        """Run LHS simulation"""
        portfolio_values = self.simulate_lhs_portfolio(time_horizon)
        final_values = portfolio_values[:, -1]
        
        return {
            'final_values': final_values,
            'mean': np.mean(final_values),
            'std': np.std(final_values),
            'percentile_5': np.percentile(final_values, 5),
            'percentile_95': np.percentile(final_values, 95),
            'all_paths': portfolio_values
        }

class MLPathGenerationMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation with ML-based path generation using neural networks"""
    
    def __init__(self, initial_value, historical_paths, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.historical_paths = historical_paths
        self.model = None
        
    def train_neural_network_paths(self):
        """Train a simple neural network to learn path patterns from historical data"""
        try:
            from sklearn.neural_network import MLPRegressor
            
            # Prepare training data
            X = self.historical_paths[:, :-1]  # All but last point
            y = np.diff(self.historical_paths, axis=1)  # Differences
            
            # Flatten for training
            X_flat = X.reshape(X.shape[0], -1)
            y_flat = y.reshape(y.shape[0], -1)
            
            # Train neural network
            self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=random_seed)
            self.model.fit(X_flat, y_flat)
            
            return True
        except ImportError:
            print("scikit-learn not available for neural network training")
            return False
    
    def generate_ml_paths(self, path_length):
        """Generate new paths using the trained neural network"""
        if self.model is None:
            # Fall back to random walks if model not trained
            paths = np.zeros((self.n_simulations, path_length))
            paths[:, 0] = self.initial_value
            
            for t in range(1, path_length):
                returns = np.random.normal(0.07, 0.14, self.n_simulations)
                paths[:, t] = paths[:, t-1] * (1 + returns)
            
            return paths
        
        # Use ML model to generate paths
        paths = np.zeros((self.n_simulations, path_length))
        paths[:, 0] = self.initial_value
        
        for i in range(self.n_simulations):
            current_path = np.zeros(path_length)
            current_path[0] = self.initial_value
            
            for t in range(1, path_length):
                # Predict next increment
                input_data = current_path[:t].reshape(1, -1)
                # Pad if input is too short
                if input_data.shape[1] < self.model.n_features_in_:
                    input_data = np.pad(input_data, ((0, 0), (0, self.model.n_features_in_ - input_data.shape[1])), 'constant')
                
                increment = self.model.predict(input_data)[0]
                current_path[t] = current_path[t-1] + np.mean(increment)
            
            paths[i] = current_path
        
        return paths
    
    def run_simulation(self, path_length=252):
        """Run ML-based path generation"""
        paths = self.generate_ml_paths(path_length)
        final_values = paths[:, -1]
        
        return {
            'final_values': final_values,
            'mean': np.mean(final_values),
            'std': np.std(final_values),
            'all_paths': paths,
            'ml_trained': self.model is not None
        }

class OutcomeClusteringMonteCarlo(MonteCarloSimulator):
    """Monte Carlo simulation with clustering of simulation outcomes for risk segmentation"""
    
    def __init__(self, initial_value, returns, volatility, n_simulations=10000, random_seed=42):
        super().__init__(n_simulations, random_seed)
        self.initial_value = initial_value
        self.returns = returns
        self.volatility = volatility
        
    def simulate_and_cluster(self, time_horizon=252, n_clusters=3):
        """Simulate paths and cluster outcomes based on risk characteristics"""
        # Generate paths
        dt = 1 / time_horizon
        paths = np.zeros((self.n_simulations, time_horizon + 1))
        paths[:, 0] = self.initial_value
        
        for t in range(time_horizon):
            z = np.random.standard_normal(self.n_simulations)
            portfolio_return = (self.returns - 0.5 * self.volatility**2) * dt + \
                               self.volatility * np.sqrt(dt) * z
            paths[:, t + 1] = paths[:, t] * (1 + portfolio_return)
        
        # Extract features for clustering
        final_values = paths[:, -1]
        max_drawdown = np.min(paths / paths[:, 0][:, None], axis=1) - 1
        volatility_paths = np.std(np.diff(paths, axis=1), axis=1)
        sharpe_ratio = (np.mean(np.diff(paths, axis=1), axis=1) / volatility_paths)
        
        features = np.column_stack([final_values, max_drawdown, volatility_paths, sharpe_ratio])
        
        # Normalize features
        features_normalized = (features - features.mean(axis=0)) / features.std(axis=0)
        
        # Cluster outcomes
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=n_clusters, random_state=random_seed, n_init=10)
            cluster_labels = kmeans.fit_predict(features_normalized)
            
            # Calculate cluster statistics
            cluster_stats = {}
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_stats[cluster_id] = {
                    'count': np.sum(cluster_mask),
                    'mean_final': np.mean(final_values[cluster_mask]),
                    'mean_drawdown': np.mean(max_drawdown[cluster_mask]),
                    'mean_sharpe': np.mean(sharpe_ratio[cluster_mask])
                }
            
            return {
                'paths': paths,
                'cluster_labels': cluster_labels,
                'cluster_stats': cluster_stats,
                'features': features,
                'kmeans': kmeans
            }
        except ImportError:
            print("scikit-learn not available for clustering")
            return {
                'paths': paths,
                'cluster_labels': None,
                'cluster_stats': None,
                'features': features
            }
    
    def run_simulation(self, time_horizon=252, n_clusters=3):
        """Run simulation with clustering"""
        return self.simulate_and_cluster(time_horizon, n_clusters)

# Example usage for advanced methods
if __name__ == "__main__":
    print("Advanced Statistical Methods and ML Integration Examples")
    print("=" * 70)
    
    # Example 1: Bayesian Monte Carlo for Endowment
    print("\n1. Bayesian Monte Carlo for Endowment Sustainability")
    prior_returns = {
        'equity': {'mean': 0.08, 'std': 0.02},
        'bond': {'mean': 0.04, 'std': 0.01}
    }
    prior_volatility = {
        'equity': {'std': 0.16},
        'bond': {'std': 0.08}
    }
    
    bayesian_mc = BayesianEndowmentMonteCarlo(
        initial_value=10000000,
        annual_payout=315000,
        prior_returns=prior_returns,
        prior_volatility=prior_volatility,
        n_simulations=5000
    )
    bayesian_results = bayesian_mc.run_simulation(years=20)
    print(f"  Posterior Mean: ${bayesian_results['posterior_mean']:,.2f}")
    print(f"  95% Credible Interval: ${bayesian_results['credible_interval_95'][0]:,.2f} - ${bayesian_results['credible_interval_95'][1]:,.2f}")
    
    # Example 2: Latin Hypercube Sampling
    print("\n2. Latin Hypercube Sampling for Efficient Simulation")
    lhs_mc = LatinHypercubeSamplingMonteCarlo(
        initial_value=1000000,
        returns=0.10,
        volatility=0.20,
        n_simulations=5000
    )
    lhs_results = lhs_mc.run_simulation(time_horizon=252)
    print(f"  Mean Final Value: ${lhs_results['mean']:,.2f}")
    print(f"  5th-95th Percentile Range: ${lhs_results['percentile_5']:,.2f} - ${lhs_results['percentile_95']:,.2f}")
    
    # Example 3: Outcome Clustering for Risk Segmentation
    print("\n3. Outcome Clustering for Risk Segmentation")
    cluster_mc = OutcomeClusteringMonteCarlo(
        initial_value=1000000,
        returns=0.10,
        volatility=0.20,
        n_simulations=5000
    )
    cluster_results = cluster_mc.run_simulation(time_horizon=252, n_clusters=3)
    
    if cluster_results['cluster_stats']:
        print("  Cluster Statistics:")
        for cluster_id, stats in cluster_results['cluster_stats'].items():
            print(f"    Cluster {cluster_id}: {stats['count']} paths, Mean Final: ${stats['mean_final']:,.2f}")
    
    print("\nAll advanced simulations completed successfully!")

# Visualization functions

def plot_simulation_histogram(data, title="Monte Carlo Simulation Results", xlabel="Value"):
    """Plot histogram of simulation results"""
    plt.figure(figsize=(12, 6))
    plt.hist(data, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(np.mean(data), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(data):,.2f}')
    plt.axvline(np.median(data), color='blue', linestyle='--', linewidth=2, label=f'Median: {np.median(data):,.2f}')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_histogram_with_kde(data, title="Histogram with KDE", xlabel="Value"):
    """Plot histogram with Kernel Density Estimation"""
    from scipy.stats import gaussian_kde
    
    plt.figure(figsize=(12, 6))
    plt.hist(data, bins=50, edgecolor='black', alpha=0.5, color='steelblue', density=True)
    
    # Add KDE
    kde = gaussian_kde(data)
    x_range = np.linspace(data.min(), data.max(), 200)
    plt.plot(x_range, kde(x_range), linewidth=3, color='red', label='KDE')
    
    plt.axvline(np.mean(data), color='blue', linestyle='--', linewidth=2, label=f'Mean: {np.mean(data):,.2f}')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_simulation_paths(paths, title="Simulation Paths", xlabel="Time", ylabel="Value"):
    """Plot simulation paths"""
    plt.figure(figsize=(14, 8))
    
    # Plot first 100 paths
    for i in range(min(100, len(paths))):
        plt.plot(paths[i], alpha=0.1, color='steelblue')
    
    # Plot mean path
    mean_path = np.mean(paths, axis=0)
    plt.plot(mean_path, linewidth=3, color='red', label='Mean Path')
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_confidence_bands(paths, title="Confidence Bands", xlabel="Time", ylabel="Value"):
    """Plot confidence bands around mean path"""
    plt.figure(figsize=(14, 8))
    
    mean_path = np.mean(paths, axis=0)
    std_path = np.std(paths, axis=0)
    
    plt.plot(mean_path, linewidth=3, color='red', label='Mean')
    plt.fill_between(range(len(mean_path)), 
                     mean_path - 1.96 * std_path,
                     mean_path + 1.96 * std_path,
                     alpha=0.3, color='steelblue', label='95% Confidence Interval')
    plt.fill_between(range(len(mean_path)), 
                     mean_path - std_path,
                     mean_path + std_path,
                     alpha=0.5, color='steelblue', label='68% Confidence Interval')
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_box_violin_comparison(data_dict, title="Box and Violin Plot Comparison"):
    """Plot both box and violin plots for comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Box plot
    axes[0].boxplot(data_dict.values(), labels=data_dict.keys(), patch_artist=True)
    axes[0].set_title('Box Plot', fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Violin plot
    parts = axes[1].violinplot(data_dict.values(), showmeans=True, showmedians=True)
    axes[1].set_xticks(np.arange(1, len(data_dict) + 1))
    axes[1].set_xticklabels(data_dict.keys())
    axes[1].set_title('Violin Plot', fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return plt

def plot_multi_series_comparison(data_dict, title="Multi-Series Comparison", xlabel="Time", ylabel="Value"):
    """Plot multiple series with confidence bands"""
    plt.figure(figsize=(14, 8))
    
    colors = ['#2b6cb0', '#e53e3e', '#38a169', '#dd6b20', '#805ad5']
    
    for i, (label, data) in enumerate(data_dict.items()):
        if isinstance(data, np.ndarray) and data.ndim == 2:
            # 2D array (multiple paths)
            mean_path = np.mean(data, axis=0)
            std_path = np.std(data, axis=0)
            x = np.arange(len(mean_path))
            plt.plot(x, mean_path, linewidth=2.5, markersize=6, label=label, color=colors[i % len(colors)])
            plt.fill_between(x, mean_path - std_path, mean_path + std_path, alpha=0.2, color=colors[i % len(colors)])
        else:
            # 1D array (single series)
            plt.plot(data, linewidth=2.5, markersize=6, label=label, color=colors[i % len(colors)])
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_survival_probability(survival_data, title="Survival Probability"):
    """Plot survival probability over time"""
    plt.figure(figsize=(12, 6))
    
    x = np.arange(len(survival_data))
    plt.plot(x, survival_data, linewidth=3, markersize=8, marker='o', color='#2b6cb0')
    plt.fill_between(x, survival_data, alpha=0.3, color='#4299e1')
    
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Survival Probability', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_risk_return_scatter(mean_returns, volatilities, labels, title="Risk-Return Tradeoff"):
    """Plot risk-return scatter for different strategies"""
    plt.figure(figsize=(12, 8))
    
    colors = ['#e53e3e', '#dd6b20', '#d69e2e', '#38a169', '#3182ce', '#805ad5']
    
    for i, (mean_return, volatility, label) in enumerate(zip(mean_returns, volatilities, labels)):
        plt.scatter(volatility, mean_return, s=500, alpha=0.7, color=colors[i % len(colors)], 
                   edgecolors='black', linewidth=2, label=label)
        plt.annotate(label, (volatility, mean_return), xytext=(5, 5), textcoords='offset points',
                   fontsize=11, fontweight='bold')
    
    plt.xlabel('Volatility (Risk)', fontsize=12)
    plt.ylabel('Mean Return', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

def plot_correlation_heatmap(data, title="Correlation Heatmap"):
    """Plot correlation heatmap for multivariate data"""
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data
    
    corr_matrix = df.corr()
    
    plt.figure(figsize=(10, 8))
    plt.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    plt.colorbar(label='Correlation Coefficient')
    
    # Add value annotations
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                    ha="center", va="center", color="black", fontweight='bold')
    
    plt.xticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns, rotation=45, ha='right')
    plt.yticks(np.arange(len(corr_matrix.columns)), corr_matrix.columns)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    return plt

def plot_dashboard_2x2(plot1_data, plot2_data, plot3_data, plot4_data, 
                       plot1_title="Plot 1", plot2_title="Plot 2", 
                       plot3_title="Plot 3", plot4_title="Plot 4",
                       main_title="Monte Carlo Simulation Dashboard"):
    """Create a 2x2 dashboard with 4 plots"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    # Plot 1: Histogram
    axes[0].hist(plot1_data, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0].axvline(np.mean(plot1_data), color='red', linestyle='--', linewidth=2)
    axes[0].set_title(plot1_title, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Line chart
    if isinstance(plot2_data, dict):
        for i, (label, data) in enumerate(plot2_data.items()):
            axes[1].plot(data, linewidth=2, label=label)
        axes[1].legend()
    else:
        axes[1].plot(plot2_data, linewidth=2)
    axes[1].set_title(plot2_title, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Box plot
    if isinstance(plot3_data, dict):
        axes[2].boxplot(plot3_data.values(), labels=plot3_data.keys(), patch_artist=True)
    else:
        axes[2].boxplot(plot3_data, patch_artist=True)
    axes[2].set_title(plot3_title, fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Scatter
    if len(plot4_data) == 2:
        axes[3].scatter(plot4_data[0], plot4_data[1], alpha=0.6, color='steelblue', edgecolors='black')
        axes[3].set_xlabel('X')
        axes[3].set_ylabel('Y')
    axes[3].set_title(plot4_title, fontweight='bold')
    axes[3].grid(True, alpha=0.3)
    
    plt.suptitle(main_title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return plt

def plot_percentile_bands(paths, title="Percentile Bands", xlabel="Time", ylabel="Value"):
    """Plot percentile bands (5th, 25th, 50th, 75th, 95th)"""
    plt.figure(figsize=(14, 8))
    
    # Calculate percentiles
    p5 = np.percentile(paths, 5, axis=0)
    p25 = np.percentile(paths, 25, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p75 = np.percentile(paths, 75, axis=0)
    p95 = np.percentile(paths, 95, axis=0)
    
    x = np.arange(len(p50))
    
    # Fill percentile bands
    plt.fill_between(x, p5, p95, alpha=0.2, color='steelblue', label='5th-95th percentile')
    plt.fill_between(x, p25, p75, alpha=0.4, color='steelblue', label='25th-75th percentile')
    
    # Plot median
    plt.plot(x, p50, linewidth=3, color='red', label='Median (50th percentile)')
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt

# Example usage
if __name__ == "__main__":
    print("Monte Carlo Simulations Portfolio")
    print("=" * 60)
    
    # Example 1: Portfolio Simulation
    print("\n1. Portfolio Simulation")
    portfolio_mc = PortfolioMonteCarlo(returns=0.10, volatility=0.20, initial_investment=100000)
    portfolio_results = portfolio_mc.run_simulation(time_horizon=252)
    print(f"   Final Value Mean: ${portfolio_results['mean']:,.2f}")
    print(f"   Probability of Profit: {portfolio_results['probability_profit']:.2%}")
    
    # Example 2: Option Pricing
    print("\n2. Option Pricing")
    option_mc = OptionPricingMonteCarlo(S=100, K=105, T=1, r=0.05, sigma=0.2)
    option_results = option_mc.run_simulation(option_type='call')
    print(f"   Call Option Price: ${option_results['option_price']:.2f}")
    
    # Example 3: VaR Calculation
    print("\n3. Value at Risk")
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, 1000)
    var_mc = RiskVaRMonteCarlo(portfolio_value=1000000, returns=returns)
    var_results = var_mc.run_simulation(confidence_level=0.95)
    print(f"   95% VaR: ${var_results['var_dollar']:,.2f}")
    print(f"   Expected Shortfall: ${var_results['cvar_dollar']:,.2f}")
    
    print("\nAll simulations completed successfully!")
