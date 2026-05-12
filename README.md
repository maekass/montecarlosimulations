# Monte Carlo Simulations Portfolio

## Abstract

This project addresses a critical gap in the application of advanced statistical and quantitative tools within impact investing and non-profit endowment management. While sophisticated Monte Carlo simulations, Bayesian methods, and machine learning techniques are standard practice in equity markets, private equity, and venture capital—where they drive portfolio optimization, risk management, and strategic decision-making—these tools remain significantly underutilized in the non-profit sector. Traditional endowment and impact investment approaches often rely on static assumptions, deterministic projections, and heuristic risk assessments that fail to capture the complex, non-linear dynamics inherent in long-term capital stewardship under uncertainty. This repository demonstrates the application of advanced quantitative methods—including Bayesian Monte Carlo simulation, Latin Hypercube Sampling, machine learning-based path generation, and outcome clustering—to non-profit endowment management, providing a framework for more robust decision-making under uncertainty. By bridging the methodological divide between for-profit quantitative finance and non-profit capital stewardship, this work aims to elevate the analytical sophistication of impact investing and endowment management, ultimately enabling more sustainable mission-driven outcomes through better-informed risk assessment and strategic planning.

A comprehensive collection of Monte Carlo simulation implementations for finance, risk management, and decision analysis, with specialized tools for non-profit endowment management.

## Overview

**What is this about?** Monte Carlo simulations are a way to predict the future by running thousands of "what if" scenarios. Think of it like playing a game thousands of times to understand all possible outcomes. Instead of guessing what might happen, we use computers to simulate many different futures and see what patterns emerge.

Monte Carlo simulations are computational algorithms that rely on repeated random sampling to obtain numerical results. This project includes implementations for:

- **Portfolio Simulation** - Simulating investment returns using Geometric Brownian Motion
- **Option Pricing** - European call and put option pricing using Monte Carlo
- **Value at Risk (VaR)** - Risk assessment and expected shortfall calculations
- **Project Cost Estimation** - Uncertainty quantification in project planning
- **Revenue Forecasting** - Multi-period revenue projection with volatility

## Non-Profit Endowment Simulations

**Why endowments need this:** Non-profit organizations rely on their endowments to fund their missions forever. But markets are unpredictable—if the market crashes right after you make a big spending commitment, you might run out of money. These simulations help organizations make smarter decisions by testing thousands of different scenarios to see how much they can safely spend without going bankrupt.

Specialized Monte Carlo tools for non-profit endowment management:

- **Sustainability Planning** - Tests whether the portfolio can support planned annual payouts (e.g., $315,000 yearly on a $10M portfolio) without depleting the principal
- **Withdrawal Strategies** - Evaluates the impact of fixed-dollar vs. percentage-based spending rules (e.g., 5% vs. 15% payout) on portfolio survival
- **Asset Allocation Testing** - Assesses the risk of different portfolios, such as comparing traditional, conservative allocations to more aggressive, modern allocations (e.g., 30% bonds/70% stocks)
- **Crisis Management** - Simulates "horrible year" scenarios, such as a 30% market drop, to test if an endowment can survive extreme volatility

### Key Metrics for Endowments

- **Probability of Survival** - Percentage of scenarios where the endowment remains above a certain threshold (e.g., a 90% chance of maintaining purchasing power)
- **End Value Distribution** - A range of potential final values rather than a single average estimate, providing a spectrum of risk
- **Median Outcome** - The most likely outcome, along with worst-case and best-case scenarios

## Multi-Language Implementations

**Why multiple languages?** Different organizations use different tools. A bank might use SQL databases, a research lab might use Julia for speed, a startup might use Ruby for web applications. By showing the same simulations in multiple languages, this project demonstrates that these techniques can be implemented anywhere—not just in one specific programming language. This also shows technical versatility to potential employers.

This project demonstrates Monte Carlo simulations across multiple programming languages to showcase versatility and technical breadth:

### Python Implementation

```python
from monte_carlo_simulations import EndowmentSustainabilityMonteCarlo

endowment_mc = EndowmentSustainabilityMonteCarlo(
    initial_value=10000000,
    annual_payout=315000,
    equity_return=0.08,
    bond_return=0.04,
    equity_volatility=0.16,
    bond_volatility=0.08,
    equity_allocation=0.70,
    inflation_rate=0.03
)

results = endowment_mc.run_simulation(years=20)
print(f"Survival Probability: {results['survival_probability']:.2%}")
```

### SQL Implementation (PostgreSQL)

```sql
-- Insert endowment parameters
INSERT INTO endowment_parameters (
    initial_value, annual_payout, equity_allocation,
    equity_return_mean, equity_return_std,
    bond_return_mean, bond_return_std,
    inflation_rate, time_horizon
) VALUES (10000000, 315000, 0.70, 0.08, 0.16, 0.04, 0.08, 0.03, 20);

-- Run Monte Carlo simulation
SELECT * FROM run_endowment_monte_carlo(1000, 20);

-- Calculate survival probability
SELECT calculate_survival_probability(0.80);
```

### Julia Implementation

```julia
endowment_mc = EndowmentSustainabilityMonteCarlo(
    initial_value=10_000_000.0,
    annual_payout=315_000.0,
    equity_return=0.08,
    bond_return=0.04,
    equity_volatility=0.16,
    bond_volatility=0.08,
    equity_allocation=0.70,
    inflation_rate=0.03,
    n_simulations=5000
)

endowment_values = simulate_endowment(endowment_mc, 20)
survival_probability = mean(endowment_values[:, end] .>= endowment_mc.initial_value * 0.8)
```

### Ruby Implementation

```ruby
endowment_mc = MonteCarlo::EndowmentSustainability.new(
  initial_value: 10_000_000.0,
  annual_payout: 315_000.0,
  equity_return: 0.08,
  bond_return: 0.04,
  equity_volatility: 0.16,
  bond_volatility: 0.08,
  equity_allocation: 0.70,
  inflation_rate: 0.03,
  n_simulations: 5000
)

results = endowment_mc.run(years: 20)
puts "Survival Probability: #{(results[:survival_probability] * 100).round(2)}%"
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Portfolio Simulation

```python
from monte_carlo_simulations import PortfolioMonteCarlo

# Simulate portfolio returns
portfolio_mc = PortfolioMonteCarlo(
    returns=0.10,           # Expected annual return
    volatility=0.20,        # Annual volatility
    initial_investment=100000
)

results = portfolio_mc.run_simulation(time_horizon=252)
print(f"Mean Final Value: ${results['mean']:,.2f}")
print(f"Probability of Profit: {results['probability_profit']:.2%}")
```

### Option Pricing

```python
from monte_carlo_simulations import OptionPricingMonteCarlo

# Price a European call option
option_mc = OptionPricingMonteCarlo(
    S=100,      # Current stock price
    K=105,      # Strike price
    T=1,        # Time to maturity (years)
    r=0.05,     # Risk-free rate
    sigma=0.2   # Volatility
)

results = option_mc.run_simulation(option_type='call')
print(f"Call Option Price: ${results['option_price']:.2f}")
```

### Value at Risk (VaR)

```python
from monte_carlo_simulations import RiskVaRMonteCarlo
import numpy as np

# Calculate VaR for a portfolio
returns = np.random.normal(0.001, 0.02, 1000)  # Historical returns
var_mc = RiskVaRMonteCarlo(portfolio_value=1000000, returns=returns)

results = var_mc.run_simulation(confidence_level=0.95)
print(f"95% VaR: ${results['var_dollar']:,.2f}")
print(f"Expected Shortfall: ${results['cvar_dollar']:,.2f}")
```

### Project Cost Estimation

```python
from monte_carlo_simulations import ProjectCostMonteCarlo

# Estimate project costs with uncertainty
cost_variations = {
    'materials': (50000, 80000, 'triangular'),
    'labor': (30000, 50000, 'normal'),
    'equipment': (20000, 35000, 'uniform')
}

cost_mc = ProjectCostMonteCarlo(base_cost=100000, cost_variations=cost_variations)
results = cost_mc.run_simulation()
print(f"Mean Total Cost: ${results['mean']:,.2f}")
print(f"90th Percentile: ${results['percentile_90']:,.2f}")
```

### Revenue Forecasting

```python
from monte_carlo_simulations import RevenueForecastMonteCarlo

# Forecast revenue over 5 years
revenue_mc = RevenueForecastMonteCarlo(
    base_revenue=1000000,
    growth_rate=0.10,
    volatility=0.15
)

results = revenue_mc.run_simulation(years=5)
print(f"Mean Year 5 Revenue: ${results['mean_final']:,.2f}")
```

## Advanced Statistical Methods & ML Integration

**What makes these "advanced"?** Traditional simulations assume we know exactly what will happen in the future (like "stocks always return 8%"). But in reality, we're uncertain about everything. Advanced methods handle this uncertainty in smarter ways: Bayesian methods let us update our beliefs as we learn more, Latin Hypercube Sampling is like a more efficient way to explore possibilities, machine learning learns patterns from historical data, and clustering groups similar outcomes together to understand risks better. These are the same techniques used by hedge funds and quantitative trading firms.

The project includes advanced simulation techniques for sophisticated endowment analysis:

### Bayesian Monte Carlo

```python
from monte_carlo_simulations import BayesianEndowmentMonteCarlo

# Define prior distributions for parameters
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
    prior_volatility=prior_volatility
)

results = bayesian_mc.run_simulation(years=20)
print(f"Posterior Mean: ${results['posterior_mean']:,.2f}")
print(f"95% Credible Interval: ${results['credible_interval_95'][0]:,.2f} - ${results['credible_interval_95'][1]:,.2f}")
```

### Latin Hypercube Sampling

```python
from monte_carlo_simulations import LatinHypercubeSamplingMonteCarlo

lhs_mc = LatinHypercubeSamplingMonteCarlo(
    initial_value=1000000,
    returns=0.10,
    volatility=0.20
)

results = lhs_mc.run_simulation(time_horizon=252)
print(f"Mean Final Value: ${results['mean']:,.2f}")
print(f"5th-95th Percentile: ${results['percentile_5']:,.2f} - ${results['percentile_95']:,.2f}")
```

### ML-Based Path Generation

```python
from monte_carlo_simulations import MLPathGenerationMonteCarlo

# Generate synthetic historical paths for training
np.random.seed(42)
historical_paths = np.zeros((100, 100))
for i in range(100):
    historical_paths[i, 0] = 1000000
    for t in range(1, 100):
        historical_paths[i, t] = historical_paths[i, t-1] * (1 + np.random.normal(0.07, 0.14))

ml_mc = MLPathGenerationMonteCarlo(
    initial_value=1000000,
    historical_paths=historical_paths
)

ml_mc.train_neural_network_paths()
results = ml_mc.run_simulation(path_length=252)
print(f"ML Generated Paths Mean: ${results['mean']:,.2f}")
```

### Outcome Clustering for Risk Segmentation

```python
from monte_carlo_simulations import OutcomeClusteringMonteCarlo

cluster_mc = OutcomeClusteringMonteCarlo(
    initial_value=1000000,
    returns=0.10,
    volatility=0.20
)

results = cluster_mc.run_simulation(time_horizon=252, n_clusters=3)

if results['cluster_stats']:
    print("Cluster Statistics:")
    for cluster_id, stats in results['cluster_stats'].items():
        print(f"  Cluster {cluster_id}: {stats['count']} paths")
        print(f"    Mean Final: ${stats['mean_final']:,.2f}")
        print(f"    Mean Drawdown: {stats['mean_drawdown']:.2%}")
        print(f"    Mean Sharpe: {stats['mean_sharpe']:.2f}")
```

## Visualizations

**Why visualizations matter:** Numbers alone can be overwhelming. A good chart can instantly show patterns that would take hours to spot in a spreadsheet. These visualizations turn thousands of simulation results into clear, actionable insights—showing you at a glance what the risks are, what the likely outcomes are, and where the dangerous scenarios might be. This is how analysts communicate complex findings to decision-makers who may not be technical.

The project includes comprehensive data visualization functions for analyzing and presenting simulation results:

### Basic Visualizations

```python
from monte_carlo_simulations import plot_simulation_histogram, plot_simulation_paths, plot_confidence_bands

# Plot histogram of results
plot_simulation_histogram(results['final_values'], title="Portfolio Final Values")
plt.show()

# Plot simulation paths
plot_simulation_paths(results['all_paths'], title="Portfolio Value Paths")
plt.show()

# Plot confidence bands
plot_confidence_bands(results['all_paths'], title="Confidence Bands")
plt.show()
```

### Advanced Visualizations

```python
from monte_carlo_simulations import (
    plot_histogram_with_kde,
    plot_box_violin_comparison,
    plot_multi_series_comparison,
    plot_survival_probability,
    plot_risk_return_scatter,
    plot_correlation_heatmap,
    plot_dashboard_2x2,
    plot_percentile_bands
)

# Histogram with Kernel Density Estimation
plot_histogram_with_kde(results['final_values'], title="Distribution with KDE")
plt.show()

# Box and Violin plot comparison
data_dict = {'Strategy A': results['final_values'][:5000], 'Strategy B': results['final_values'][5000:]}
plot_box_violin_comparison(data_dict, title="Strategy Comparison")
plt.show()

# Multi-series comparison with confidence bands
plot_multi_series_comparison(allocation_results, title="Asset Allocation Comparison")
plt.show()

# Survival probability over time
plot_survival_probability(survival_data, title="Endowment Survival Probability")
plt.show()

# Risk-return scatter plot
plot_risk_return_scatter(mean_returns, volatilities, strategy_names, title="Risk-Return Tradeoff")
plt.show()

# Correlation heatmap
plot_correlation_heatmap(correlation_data, title="Correlation Matrix")
plt.show()

# 2x2 dashboard
plot_dashboard_2x2(data1, data2, data3, data4, 
                   plot1_title="Histogram", plot2_title="Line Chart",
                   plot3_title="Box Plot", plot4_title="Scatter",
                   main_title="Monte Carlo Dashboard")
plt.show()

# Percentile bands (5th, 25th, 50th, 75th, 95th)
plot_percentile_bands(results['all_paths'], title="Percentile Bands")
plt.show()
```

## Project Structure

```
monte-carlo-simulations/
├── monte_carlo_simulations.py  # Main simulation classes
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── examples/                    # Example notebooks (optional)
```

## Simulation Classes

### PortfolioMonteCarlo
- Simulates portfolio returns using Geometric Brownian Motion
- Returns mean, median, standard deviation, and probability of profit
- Supports custom time horizons and volatility parameters

### OptionPricingMonteCarlo
- Prices European call and put options
- Uses Geometric Brownian Motion for stock price paths
- Returns option price with standard error

### RiskVaRMonteCarlo
- Calculates Value at Risk (VaR) and Expected Shortfall (CVaR)
- Uses historical return distribution for simulation
- Supports custom confidence levels

### ProjectCostMonteCarlo
- Estimates total project cost with component-level uncertainty
- Supports multiple probability distributions (uniform, triangular, normal)
- Returns statistical summary of cost distribution

### RevenueForecastMonteCarlo
- Forecasts revenue over multiple periods
- Accounts for growth rate uncertainty and volatility
- Returns distribution of final year revenue

## Dependencies

- numpy >= 1.24.0
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scipy >= 1.10.0

## License

MIT License

## Author

Created as a demonstration of Monte Carlo simulation techniques for financial and risk analysis.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
