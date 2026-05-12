# Monte Carlo Simulations for Non-Profit Endowments

## Overview

This document provides Monte Carlo simulation tools for non-profit endowment management, including sustainability planning, withdrawal strategies, asset allocation testing, and crisis management scenarios.

---

## Key Uses in Non-Profit Endowments

### Sustainability Planning
Tests whether the portfolio can support planned annual payouts (e.g., $315,000 yearly on a $10M portfolio) without depleting the principal.

### Withdrawal Strategies
Evaluates the impact of fixed-dollar vs. percentage-based spending rules (e.g., 5% vs. 15% payout) on portfolio survival.

### Asset Allocation Testing
Assesses the risk of different portfolios, such as comparing traditional, conservative allocations to more aggressive, modern allocations (e.g., 30% bonds/70% stocks).

### Crisis Management
Simulates "horrible year" scenarios, such as a 30% market drop, to test if an endowment can survive extreme volatility.

---

## Typical Simulation Parameters

- **Initial Portfolio Value**: Starting balance
- **Asset Class Returns & Volatility**: Based on 50-year historical averages or forecasted data (equities vs. bonds)
- **Spending Amount**: Fixed amount or a percentage of assets, often adjusted for inflation
- **Time Horizon**: Often simulated over 5+ years for tactical planning or much longer for perpetuity goals

---

## Key Metrics and Results

- **Probability of Survival**: Percentage of scenarios where the endowment remains above a certain threshold (e.g., a 90% chance of maintaining purchasing power)
- **End Value Distribution**: A range of potential final values rather than a single average estimate, providing a spectrum of risk
- **Median Outcome**: The most likely outcome, along with worst-case and best-case scenarios

---

## Simulation Classes

### 1. Endowment Sustainability Planning

Tests whether the portfolio can support planned annual payouts without depleting principal.

**Parameters:**
- `initial_value`: Starting portfolio value
- `annual_payout`: Fixed annual spending amount
- `equity_return`: Expected equity return
- `bond_return`: Expected bond return
- `equity_volatility`: Equity volatility
- `bond_volatility`: Bond volatility
- `equity_allocation`: Percentage in equities
- `inflation_rate`: Annual inflation rate

**Example:**
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
print(f"Mean Final Value: ${results['mean_final']:,.2f}")
```

---

### 2. Withdrawal Strategy Comparison

Compares fixed-dollar vs. percentage-based spending rules.

**Parameters:**
- `initial_value`: Starting portfolio value
- `returns`: Expected portfolio return
- `volatility`: Portfolio volatility

**Example:**
```python
from monte_carlo_simulations import WithdrawalStrategyMonteCarlo

withdrawal_mc = WithdrawalStrategyMonteCarlo(
    initial_value=10000000,
    returns=0.07,
    volatility=0.14
)

results = withdrawal_mc.run_simulation(
    fixed_amount=315000,
    percentage_rate=0.05,
    years=20
)

print(f"Fixed Strategy Survival: {results['fixed_survival_rate']:.2%}")
print(f"Percentage Strategy Survival: {results['percentage_survival_rate']:.2%}")
```

---

### 3. Asset Allocation Testing

Compares different portfolio allocations (conservative vs. aggressive).

**Parameters:**
- `initial_value`: Starting portfolio value
- `allocations`: Dictionary of allocation strategies
- `returns_dict`: Expected returns for each asset class
- `volatility_dict`: Volatility for each asset class

**Example:**
```python
from monte_carlo_simulations import AssetAllocationMonteCarlo

allocations = {
    'Conservative': {'equity': 0.30, 'bond': 0.70},
    'Balanced': {'equity': 0.60, 'bond': 0.40},
    'Aggressive': {'equity': 0.70, 'bond': 0.30}
}

returns_dict = {'equity': 0.08, 'bond': 0.04}
volatility_dict = {'equity': 0.16, 'bond': 0.08}

allocation_mc = AssetAllocationMonteCarlo(
    initial_value=10000000,
    allocations=allocations,
    returns_dict=returns_dict,
    volatility_dict=volatility_dict
)

results = allocation_mc.run_simulation(years=20)

for alloc_name, result in results.items():
    print(f"{alloc_name}: Mean ${result['mean_final']:,.2f}")
```

---

### 4. Crisis Management

Simulates extreme volatility scenarios (e.g., 30% market drop).

**Parameters:**
- `initial_value`: Starting portfolio value
- `normal_return`: Normal market return
- `normal_volatility`: Normal market volatility
- `crisis_drop`: Percentage drop during crisis (e.g., -0.30 for 30%)
- `crisis_probability`: Probability of crisis year

**Example:**
```python
from monte_carlo_simulations import CrisisManagementMonteCarlo

crisis_mc = CrisisManagementMonteCarlo(
    initial_value=10000000,
    normal_return=0.07,
    normal_volatility=0.14,
    crisis_drop=-0.30,
    crisis_probability=0.05
)

results = crisis_mc.run_simulation(years=20)
print(f"Survival Rate: {results['survival_rate']:.2%}")
print(f"Mean Final Value: ${results['mean_final']:,.2f}")
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Dependencies

- numpy >= 1.24.0
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scipy >= 1.10.0

---

## Visualization Functions

### Histogram of Results
```python
from monte_carlo_simulations import plot_simulation_histogram

plot_simulation_histogram(results['final_values'], title="Endowment Final Values")
plt.show()
```

### Simulation Paths
```python
from monte_carlo_simulations import plot_simulation_paths

plot_simulation_paths(results['endowment_values'], title="Endowment Value Paths")
plt.show()
```

### Confidence Bands
```python
from monte_carlo_simulations import plot_confidence_bands

plot_confidence_bands(results['endowment_values'], title="Confidence Bands")
plt.show()
```

---

## Quick Reference Table

| Simulation | Key Output | Use Case |
|------------|-------------|----------|
| Sustainability | Survival probability, final value distribution | Can we afford our spending? |
| Withdrawal Strategies | Survival rate comparison | Fixed vs. percentage spending |
| Asset Allocation | Risk-return comparison | Conservative vs. aggressive |
| Crisis Management | Survival under stress | What if markets crash? |

---

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Import the simulation class you need
3. Set parameters based on your endowment
4. Run simulation with `run_simulation()`
5. Visualize results with built-in plotting functions

---

## License

MIT License
