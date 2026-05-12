# Monte Carlo Simulations for Non-Profit Endowments

## Overview

This document provides Monte Carlo simulation tools for non-profit endowment management, including sustainability planning, withdrawal strategies, asset allocation testing, and crisis management scenarios.

---

## Key Uses in Non-Profit Endowments

### 🎯 Sustainability Planning
Tests whether the portfolio can support planned annual payouts (e.g., $315,000 yearly on a $10M portfolio) without depleting the principal.

**Visual Output:**
```
📊 Endowment Value Over 20 Years
$10M ────────────────────┐
      ╱                  ╲
$8M  ╱                    ╲
     ╱                      ╲
$6M ╱                        ╲
    ╱                          ╲
$4M ╱                            ╲
   ╱                              ╲
$2M ╱                                ╲
  ╱                                  ╲
$0  └─────────────────────────────────
   0    5    10   15   20   Years
```

### 💸 Withdrawal Strategies
Evaluates the impact of fixed-dollar vs. percentage-based spending rules (e.g., 5% vs. 15% payout) on portfolio survival.

**Visual Comparison:**
```
Strategy Comparison (20-Year Horizon)
┌─────────────────┬─────────────┬─────────────┐
│ Strategy        │ Survival    │ Final Value │
├─────────────────┼─────────────┼─────────────┤
│ Fixed $315K     │     78%     │    $8.2M    │
│ 5% Percentage   │     85%     │    $9.1M    │
│ 10% Percentage  │     62%     │    $6.3M    │
│ 15% Percentage  │     41%     │    $4.1M    │
└─────────────────┴─────────────┴─────────────┘
```

### 📈 Asset Allocation Testing
Assesses the risk of different portfolios, such as comparing traditional, conservative allocations to more aggressive, modern allocations (e.g., 30% bonds/70% stocks).

**Risk-Return Tradeoff:**
```
Portfolio Performance Comparison
Conservative (30/70):   ◆ Low Risk, Low Return
Balanced (60/40):       ◆ Moderate Risk, Moderate Return  
Aggressive (70/30):     ◆ High Risk, High Return
Ultra-Aggressive (90/10):◆ Very High Risk, Very High Return

Risk → ──────────────────────────→
       ●    ●   ●         ●
Return → ──────────────────────────→
```

### 🚨 Crisis Management
Simulates "horrible year" scenarios, such as a 30% market drop, to test if an endowment can survive extreme volatility.

**Crisis Scenario Impact:**
```
Market Crash Simulation (-30% Drop)
Normal Market: ──────────────────────
Crisis Year:   ╲_____________________
               ╲
Recovery:      ╱╲___________________
               ╱  ╲
Survival Rate: 73% (vs 95% in normal market)
```

---

## Typical Simulation Parameters

| Parameter | Typical Range | Impact |
|-----------|---------------|---------|
| **Initial Portfolio Value** | $1M - $100M+ | Larger portfolios have more resilience |
| **Equity Returns** | 6-10% annually | Higher returns increase sustainability |
| **Bond Returns** | 2-5% annually | Provides stability but lower growth |
| **Equity Volatility** | 12-20% | Higher volatility = more uncertainty |
| **Inflation Rate** | 2-4% | Erodes purchasing power over time |
| **Time Horizon** | 5-50+ years | Longer horizons show more variation |

---

## Key Metrics and Results

### 📊 Probability of Survival
Percentage of scenarios where the endowment remains above a certain threshold (e.g., a 90% chance of maintaining purchasing power)

**Survival Probability Heatmap:**
```
Spending Rate →
        3%    5%    7%    9%   11%
Time  ┌───────────────────────────────
20yr  │ 98%  92%  78%  62%  41%
30yr  │ 95%  85%  68%  48%  25%
50yr  │ 89%  73%  52%  31%  12%
```

### 📈 End Value Distribution
A range of potential final values rather than a single average estimate, providing a spectrum of risk

**Distribution Visualization:**
```
Final Portfolio Value Distribution
$15M ────────┐
            ╱╲
$12M ──────╱   ╲─────┐
          ╱     ╲   ╱
$9M  ────╱       ╲─╱───┐
        ╱         ╲     ╲
$6M  ──╱           ╲     ╲─
      ╱             ╲     ╲
$3M  ╱               ╲─────╲
    └───────────────────────
    P5   P25  Median  P75  P95
```

### 🎯 Median Outcome
The most likely outcome, along with worst-case and best-case scenarios

**Scenario Analysis:**
```
$10M Endowment, 5% Spending Rate
┌─────────────────────────────────────┐
│ Best Case (95th percentile): $15.2M │
│ Median (50th percentile): $9.1M     │
│ Worst Case (5th percentile): $4.3M   │
└─────────────────────────────────────┘
```

---

## Advanced Visualization Examples

### 📊 Multi-Panel Dashboard
```
┌─────────────────┬─────────────────┐
│  Histogram      │  Survival Curve │
│                 │                 │
│   ██████        │ 100% ────────┐  │
│  ████████       │  90% ─────╱ │  │
│ ███████████     │  80% ────╱  │  │
│██████████████   │  70% ───╱   │  │
│                 │     ──╱    │  │
└─────────────────┼─────────────────┤
│  Path           │  Risk Matrix    │
│  Visualization  │                 │
│  ╱╲╱╲╱╲         │  ● Low Risk     │
│ ╱  ╲╱  ╲╱       │  ●●● Medium     │
│╱    ╲    ╲      │  ●●●●● High     │
│                 │                 │
└─────────────────┴─────────────────┘
```

### 🔄 Dynamic Path Visualization
```
Monte Carlo Simulation Paths
$12M ────────────────┐
      ╱╲           ╱╲
$10M ──╱  ╲╱╲╱╱╱╱╲╱  ╲───
     ╱    ╲       ╱    ╲
$8M  ╱      ╲╱╱╱╱╲      ╲
    ╱              ╱    ╲
$6M ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╲
  └─────────────────────────
   0    5    10   15   20   Years
   (1000+ simulated paths)
```

### 📊 Risk Segmentation Clusters
```
Outcome Clustering Analysis
┌─────────────────────────────────┐
│ 🔵 Cluster 1: Conservative     │
│    • 45% of scenarios           │
│    • Low risk, steady returns   │
│    • Survival: 95%              │
├─────────────────────────────────┤
│ 🟢 Cluster 2: Moderate          │
│    • 35% of scenarios           │
│    • Balanced risk/return       │
│    • Survival: 82%              │
├─────────────────────────────────┤
│ 🔴 Cluster 3: Aggressive        │
│    • 20% of scenarios           │
│    • High risk, high returns    │
│    • Survival: 61%              │
└─────────────────────────────────┘
```

---

## Implementation Quick Start

### 🚀 Getting Started
1. **Choose Your Language**: Python, SQL, Julia, or Ruby
2. **Set Parameters**: Initial value, spending rate, asset allocation
3. **Run Simulation**: 1,000-10,000 scenarios recommended
4. **Analyze Results**: Focus on survival probability and risk metrics

### 📋 Sample Parameters
```
Conservative Endowment:
• Initial Value: $10,000,000
• Annual Spending: $350,000 (3.5%)
• Asset Mix: 40% Stocks, 60% Bonds
• Time Horizon: 30 years
• Expected Survival: 89%

Aggressive Endowment:
• Initial Value: $10,000,000  
• Annual Spending: $500,000 (5%)
• Asset Mix: 70% Stocks, 30% Bonds
• Time Horizon: 30 years
• Expected Survival: 73%
```

---

## Key Takeaways

✅ **Higher spending rates = lower survival probability**
✅ **More stocks = higher returns but more volatility**  
✅ **Longer time horizons show more variation**
✅ **Crisis scenarios can significantly impact outcomes**
✅ **Diversification helps manage risk**

---

## Next Steps

1. **Run your own simulations** using the provided code
2. **Adjust parameters** to match your specific situation
3. **Compare scenarios** to find optimal spending rate
4. **Monitor regularly** and adjust as conditions change

---

*This document provides a visual approach to understanding Monte Carlo simulations for non-profit endowment management. For detailed implementation, see the full code repository.*
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
