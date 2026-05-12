# Monte Carlo Simulations Portfolio

A comprehensive collection of Monte Carlo simulation implementations for finance, risk management, and decision analysis, with specialized tools for non-profit endowment management.

## Overview

Monte Carlo simulations are computational algorithms that rely on repeated random sampling to obtain numerical results. This project includes implementations for:

- **Portfolio Simulation** - Simulating investment returns using Geometric Brownian Motion
- **Option Pricing** - European call and put option pricing using Monte Carlo
- **Value at Risk (VaR)** - Risk assessment and expected shortfall calculations
- **Project Cost Estimation** - Uncertainty quantification in project planning
- **Revenue Forecasting** - Multi-period revenue projection with volatility

## Non-Profit Endowment Simulations

Specialized Monte Carlo tools for non-profit endowment management:

- **Sustainability Planning** - Tests whether the portfolio can support planned annual payouts (e.g., $315,000 yearly on a $10M portfolio) without depleting the principal
- **Withdrawal Strategies** - Evaluates the impact of fixed-dollar vs. percentage-based spending rules (e.g., 5% vs. 15% payout) on portfolio survival
- **Asset Allocation Testing** - Assesses the risk of different portfolios, such as comparing traditional, conservative allocations to more aggressive, modern allocations (e.g., 30% bonds/70% stocks)
- **Crisis Management** - Simulates "horrible year" scenarios, such as a 30% market drop, to test if an endowment can survive extreme volatility

### Key Metrics for Endowments

- **Probability of Survival** - Percentage of scenarios where the endowment remains above a certain threshold (e.g., a 90% chance of maintaining purchasing power)
- **End Value Distribution** - A range of potential final values rather than a single average estimate, providing a spectrum of risk
- **Median Outcome** - The most likely outcome, along with worst-case and best-case scenarios

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

## Visualizations

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
