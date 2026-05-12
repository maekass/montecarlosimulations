"""
Tableau Integration for Monte Carlo Simulations
This module prepares data for Tableau visualization and provides examples
of how to create interactive dashboards for endowment analysis.
"""

import pandas as pd
import numpy as np
from monte_carlo_simulations import (
    EndowmentSustainabilityMonteCarlo,
    BayesianEndowmentMonteCarlo,
    LatinHypercubeSamplingMonteCarlo,
    OutcomeClusteringMonteCarlo
)
import json

class TableauDataPrep:
    """Prepare Monte Carlo simulation data for Tableau visualization"""
    
    def __init__(self):
        self.data = {}
        
    def prepare_endowment_data(self, n_simulations=1000, years=20):
        """Generate endowment simulation data for Tableau"""
        
        # Run different simulation types
        endowment_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=10000000,
            annual_payout=315000,
            equity_return=0.08,
            bond_return=0.04,
            equity_volatility=0.16,
            bond_volatility=0.08,
            equity_allocation=0.70,
            inflation_rate=0.03,
            n_simulations=n_simulations
        )
        
        endowment_results = endowment_mc.run_simulation(years)
        
        # Create long-format data for Tableau
        tableau_data = []
        
        for sim_id in range(n_simulations):
            for year in range(years + 1):
                tableau_data.append({
                    'Simulation_ID': sim_id + 1,
                    'Year': year,
                    'Portfolio_Value': endowment_results['endowment_values'][sim_id, year],
                    'Simulation_Type': 'Standard',
                    'Initial_Value': 10000000,
                    'Annual_Payout': 315000,
                    'Equity_Allocation': 0.70,
                    'Inflation_Rate': 0.03
                })
        
        return pd.DataFrame(tableau_data)
    
    def prepare_strategy_comparison(self, n_simulations=1000, years=20):
        """Compare different withdrawal strategies for Tableau"""
        
        strategies = [
            {'name': 'Fixed $315K', 'payout': 315000, 'type': 'fixed'},
            {'name': '3% Percentage', 'payout': 0.03, 'type': 'percentage'},
            {'name': '5% Percentage', 'payout': 0.05, 'type': 'percentage'},
            {'name': '7% Percentage', 'payout': 0.07, 'type': 'percentage'},
            {'name': '10% Percentage', 'payout': 0.10, 'type': 'percentage'}
        ]
        
        comparison_data = []
        
        for strategy in strategies:
            for sim_id in range(n_simulations):
                portfolio_value = 10000000
                
                for year in range(years + 1):
                    # Calculate payout based on strategy type
                    if strategy['type'] == 'fixed':
                        payout = strategy['payout']
                    else:
                        payout = portfolio_value * strategy['payout']
                    
                    # Store current year data
                    comparison_data.append({
                        'Simulation_ID': sim_id + 1,
                        'Strategy': strategy['name'],
                        'Strategy_Type': strategy['type'],
                        'Year': year,
                        'Portfolio_Value': portfolio_value,
                        'Annual_Payout': payout,
                        'Payout_Rate': payout / 10000000 if year == 0 else payout / portfolio_value
                    })
                    
                    # Simulate next year
                    if year < years:
                        equity_return = np.random.normal(0.08, 0.16)
                        bond_return = np.random.normal(0.04, 0.08)
                        portfolio_return = 0.7 * equity_return + 0.3 * bond_return
                        portfolio_value = portfolio_value * (1 + portfolio_return) - payout
                        portfolio_value = max(portfolio_value, 0)
        
        return pd.DataFrame(comparison_data)
    
    def prepare_allocation_comparison(self, n_simulations=1000, years=20):
        """Compare different asset allocations for Tableau"""
        
        allocations = [
            {'name': 'Conservative', 'equity': 0.30, 'bond': 0.70},
            {'name': 'Balanced', 'equity': 0.60, 'bond': 0.40},
            {'name': 'Aggressive', 'equity': 0.70, 'bond': 0.30},
            {'name': 'Very Aggressive', 'equity': 0.90, 'bond': 0.10}
        ]
        
        allocation_data = []
        
        for allocation in allocations:
            for sim_id in range(n_simulations):
                portfolio_value = 10000000
                
                for year in range(years + 1):
                    allocation_data.append({
                        'Simulation_ID': sim_id + 1,
                        'Allocation_Strategy': allocation['name'],
                        'Equity_Allocation': allocation['equity'],
                        'Bond_Allocation': allocation['bond'],
                        'Year': year,
                        'Portfolio_Value': portfolio_value
                    })
                    
                    # Simulate next year
                    if year < years:
                        equity_return = np.random.normal(0.08, 0.16)
                        bond_return = np.random.normal(0.04, 0.08)
                        portfolio_return = (allocation['equity'] * equity_return + 
                                          allocation['bond'] * bond_return)
                        portfolio_value = portfolio_value * (1 + portfolio_return) - 315000
                        portfolio_value = max(portfolio_value, 0)
        
        return pd.DataFrame(allocation_data)
    
    def prepare_crisis_scenarios(self, n_simulations=1000, years=20):
        """Generate crisis scenario data for Tableau"""
        
        scenarios = [
            {'name': 'Normal Market', 'crisis_prob': 0.0, 'crisis_drop': 0.0},
            {'name': 'Occasional Crisis', 'crisis_prob': 0.05, 'crisis_drop': -0.20},
            {'name': 'Frequent Crisis', 'crisis_prob': 0.10, 'crisis_drop': -0.30},
            {'name': 'Severe Crisis', 'crisis_prob': 0.15, 'crisis_drop': -0.40}
        ]
        
        crisis_data = []
        
        for scenario in scenarios:
            for sim_id in range(n_simulations):
                portfolio_value = 10000000
                
                for year in range(years + 1):
                    crisis_data.append({
                        'Simulation_ID': sim_id + 1,
                        'Scenario': scenario['name'],
                        'Crisis_Probability': scenario['crisis_prob'],
                        'Crisis_Drop': scenario['crisis_drop'],
                        'Year': year,
                        'Portfolio_Value': portfolio_value,
                        'Is_Crisis_Year': 0
                    })
                    
                    # Simulate next year
                    if year < years:
                        # Check if crisis occurs
                        is_crisis = np.random.random() < scenario['crisis_prob']
                        
                        if is_crisis:
                            portfolio_return = scenario['crisis_drop']
                            crisis_indicator = 1
                        else:
                            equity_return = np.random.normal(0.08, 0.16)
                            bond_return = np.random.normal(0.04, 0.08)
                            portfolio_return = 0.7 * equity_return + 0.3 * bond_return
                            crisis_indicator = 0
                        
                        portfolio_value = portfolio_value * (1 + portfolio_return) - 315000
                        portfolio_value = max(portfolio_value, 0)
                        
                        # Update crisis indicator for next year
                        crisis_data[-1]['Is_Crisis_Year'] = crisis_indicator
        
        return pd.DataFrame(crisis_data)
    
    def export_for_tableau(self, data, filename):
        """Export data to CSV for Tableau import"""
        data.to_csv(filename, index=False)
        print(f"Data exported to {filename} ({len(data)} rows)")
    
    def create_tableau_data_extract(self):
        """Create comprehensive data extract for Tableau"""
        
        print("Generating Tableau data extracts...")
        
        # Generate all datasets
        endowment_data = self.prepare_endowment_data(500, 20)
        strategy_data = self.prepare_strategy_comparison(300, 20)
        allocation_data = self.prepare_allocation_comparison(300, 20)
        crisis_data = self.prepare_crisis_scenarios(400, 20)
        
        # Export to CSV files
        self.export_for_tableau(endowment_data, 'tableau_endowment_simulations.csv')
        self.export_for_tableau(strategy_data, 'tableau_strategy_comparison.csv')
        self.export_for_tableau(allocation_data, 'tableau_allocation_comparison.csv')
        self.export_for_tableau(crisis_data, 'tableau_crisis_scenarios.csv')
        
        # Create summary statistics for Tableau
        summary_stats = self.create_summary_statistics(
            endowment_data, strategy_data, allocation_data, crisis_data
        )
        self.export_for_tableau(summary_stats, 'tableau_summary_statistics.csv')
        
        print("All Tableau data extracts created successfully!")
    
    def create_summary_statistics(self, endowment_data, strategy_data, allocation_data, crisis_data):
        """Create summary statistics for Tableau dashboard"""
        
        stats = []
        
        # Endowment statistics
        final_values = endowment_data[endowment_data['Year'] == 20]['Portfolio_Value']
        stats.append({
            'Metric': 'Endowment Survival Rate',
            'Value': (final_values >= 8000000).mean() * 100,
            'Category': 'Endowment',
            'Unit': 'Percentage'
        })
        
        stats.append({
            'Metric': 'Mean Final Value',
            'Value': final_values.mean(),
            'Category': 'Endowment',
            'Unit': 'Dollars'
        })
        
        # Strategy comparison
        strategy_survival = strategy_data[strategy_data['Year'] == 20].groupby('Strategy')['Portfolio_Value'].apply(
            lambda x: (x >= 8000000).mean() * 100
        ).reset_index()
        
        for _, row in strategy_survival.iterrows():
            stats.append({
                'Metric': f'Survival Rate - {row["Strategy"]}',
                'Value': row['Portfolio_Value'],
                'Category': 'Strategy',
                'Unit': 'Percentage'
            })
        
        # Allocation comparison
        allocation_final = allocation_data[allocation_data['Year'] == 20].groupby('Allocation_Strategy')['Portfolio_Value'].mean().reset_index()
        
        for _, row in allocation_final.iterrows():
            stats.append({
                'Metric': f'Mean Final Value - {row["Allocation_Strategy"]}',
                'Value': row['Portfolio_Value'],
                'Category': 'Allocation',
                'Unit': 'Dollars'
            })
        
        return pd.DataFrame(stats)

def create_tableau_workbook_guide():
    """Create a guide for building Tableau dashboards"""
    
    guide = """
# Tableau Dashboard Guide for Monte Carlo Simulations

## Dashboard 1: Endowment Sustainability
### Data Source: tableau_endowment_simulations.csv

#### Sheets to Create:
1. **Portfolio Value Over Time**
   - Drag Year to Columns
   - Drag Portfolio_Value to Rows (set to AVG)
   - Drag Simulation_ID to Detail
   - Set chart type to Lines
   - Add reference line at $8M (80% threshold)

2. **Final Value Distribution**
   - Drag Portfolio_Value to Columns (filtered to Year = 20)
   - Set chart type to Histogram
   - Add reference lines for percentiles

3. **Survival Probability Heatmap**
   - Create calculated field: Is_Surviving = IF Portfolio_Value >= 8000000 THEN 1 ELSE 0 END
   - Drag Year to Columns, Is_Surviving to Rows (set to AVG)
   - Set chart type to Heat Map

## Dashboard 2: Strategy Comparison
### Data Source: tableau_strategy_comparison.csv

#### Sheets to Create:
1. **Strategy Survival Rates**
   - Filter to Year = 20
   - Drag Strategy to Columns, Portfolio_Value to Rows (set to AVG)
   - Add reference line at $8M

2. **Payout Impact Analysis**
   - Drag Year to Columns, Payout_Rate to Rows (set to AVG)
   - Drag Strategy to Color
   - Set chart type to Lines

3. **Strategy Performance Matrix**
   - Drag Strategy to Rows, Portfolio_Value to Columns (set to AVG)
   - Set chart type to Bar Chart
   - Add color coding for survival rates

## Dashboard 3: Risk Analysis
### Data Source: tableau_allocation_comparison.csv, tableau_crisis_scenarios.csv

#### Sheets to Create:
1. **Risk-Return Scatter Plot**
   - Create calculated fields for Risk (STDDEV) and Return (AVG)
   - Drag Equity_Allocation to Size, Portfolio_Value to Color
   - Set chart type to Scatter Plot

2. **Crisis Impact Visualization**
   - Drag Year to Columns, Portfolio_Value to Rows (set to AVG)
   - Drag Scenario to Color
   - Drag Is_Crisis_Year to Shape

## Dashboard 4: Executive Summary
### Data Source: tableau_summary_statistics.csv

#### Sheets to Create:
1. **Key Metrics KPIs**
   - Drag Metric to Rows, Value to Columns
   - Set chart type to Bar Chart
   - Add color coding by Category

2. **Performance Comparison**
   - Create calculated fields for benchmarks
   - Add trend lines and reference lines

## Dashboard Layout Tips:
- Use size 14-16pt fonts for readability
- Add color-coded legends (Green = Good, Yellow = Caution, Red = Risk)
- Include filters for Simulation_ID, Year, Strategy
- Add tooltips with detailed metrics
- Use actions for drill-down capabilities
- Include export options for PDF/Excel

## Calculated Fields to Create:
```
Survival Rate: 
IF [Portfolio_Value] >= [Initial_Value] * 0.8 THEN 1 ELSE 0 END

Payout Ratio:
[Annual_Payout] / [Portfolio_Value]

Years to Depletion:
IF [Portfolio_Value] <= 0 THEN [Year] END

Risk Level:
IF [Equity_Allocation] <= 0.4 THEN "Low"
ELSEIF [Equity_Allocation] <= 0.7 THEN "Medium"
ELSE "High" END
```
"""
    
    with open('tableau_dashboard_guide.md', 'w') as f:
        f.write(guide)
    
    print("Tableau dashboard guide created: tableau_dashboard_guide.md")

if __name__ == "__main__":
    # Create Tableau data extracts
    tableau_prep = TableauDataPrep()
    tableau_prep.create_tableau_data_extract()
    
    # Create dashboard guide
    create_tableau_workbook_guide()
    
    print("\nTableau integration complete!")
    print("Files created:")
    print("- tableau_endowment_simulations.csv")
    print("- tableau_strategy_comparison.csv") 
    print("- tableau_allocation_comparison.csv")
    print("- tableau_crisis_scenarios.csv")
    print("- tableau_summary_statistics.csv")
    print("- tableau_dashboard_guide.md")
