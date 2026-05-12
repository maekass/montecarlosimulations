"""
Case Studies and Examples for Monte Carlo Endowment Simulations
This module contains practical case studies for different organization types
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from monte_carlo_simulations import EndowmentSustainabilityMonteCarlo


class CaseStudyExamples:
    """Collection of case study examples for different organization types"""
    
    @staticmethod
    def university_endowment_case_study():
        """
        University Endowment Case Study
        Organization: State University (Mid-sized public university)
        Endowment: $850 million
        Current Spending: 4.8% annually ($40.8M)
        Mission: Fund scholarships, faculty positions, research programs
        """
        print("=== UNIVERSITY ENDOWMENT CASE STUDY ===")
        print("Organization: State University")
        print("Endowment: $850 million")
        print("Current Spending: 4.8% annually ($40.8M)")
        print("Mission: Fund scholarships, faculty positions, research programs")
        print()
        
        # University-specific parameters
        university_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=850000000,       # $850M endowment
            annual_payout=40800000,        # $40.8M annual spending (4.8%)
            equity_return=0.075,           # Conservative university returns
            bond_return=0.035,             # Stable bond returns
            equity_volatility=0.14,        # Moderate volatility
            bond_volatility=0.06,          # Low bond volatility
            equity_allocation=0.60,        # Balanced allocation
            inflation_rate=0.030,          # Higher education inflation
            n_simulations=5000             # High accuracy
        )
        
        # Run 25-year simulation
        results = university_mc.run_simulation(years=25)
        
        print("BASELINE RESULTS:")
        print(f"Survival Probability (25 years): {results['survival_probability']:.2%}")
        print(f"Mean Final Value: ${results['mean_final']:,.0f}")
        print(f"Median Final Value: ${results['median_final']:,.0f}")
        print(f"5th Percentile: ${results['p5_final']:,.0f}")
        print(f"95th Percentile: ${results['p95_final']:,.0f}")
        print()
        
        # Test different spending scenarios
        spending_scenarios = [
            {"name": "Conservative", "rate": 0.04, "description": "Focus on preservation"},
            {"name": "Current", "rate": 0.048, "description": "Current policy"},
            {"name": "Moderate", "rate": 0.055, "description": "Enhanced programs"},
            {"name": "Aggressive", "rate": 0.065, "description": "Excellence initiative"}
        ]
        
        print("ACADEMIC SPENDING SCENARIOS:")
        for scenario in spending_scenarios:
            payout = 850000000 * scenario["rate"]
            mc = EndowmentSustainabilityMonteCarlo(
                initial_value=850000000,
                annual_payout=payout,
                equity_return=0.075,
                bond_return=0.035,
                equity_volatility=0.14,
                bond_volatility=0.06,
                equity_allocation=0.60,
                inflation_rate=0.030,
                n_simulations=3000
            )
            
            results = mc.run_simulation(years=25)
            annual_funding = payout / 1000000
            print(f"{scenario['name']:12} ({scenario['rate']:.1%}): "
                  f"Survival {results['survival_probability']:.1%}, "
                  f"Annual Funding ${annual_funding:.1f}M")
        
        print()
        print("RECOMMENDATIONS:")
        print("1. Adopt 4.5% spending rate ($38.3M annually) for balance")
        print("2. Create 'excellence fund' for special initiatives with separate funding")
        print("3. Implement 3-year rolling average for spending calculations")
        print("4. Build $100M reserve for economic downturns")
        print()
        
        return results
    
    @staticmethod
    def healthcare_foundation_case_study():
        """
        Healthcare Foundation Case Study
        Organization: Regional Healthcare Foundation
        Endowment: $125 million
        Current Spending: 5.2% annually ($6.5M)
        Mission: Fund community health programs, medical research, clinic support
        Challenge: High healthcare inflation vs. investment returns
        """
        print("=== HEALTHCARE FOUNDATION CASE STUDY ===")
        print("Organization: Regional Healthcare Foundation")
        print("Endowment: $125 million")
        print("Current Spending: 5.2% annually ($6.5M)")
        print("Mission: Fund community health programs, medical research, clinic support")
        print("Challenge: High healthcare inflation vs. investment returns")
        print()
        
        # Healthcare foundation with unique challenges
        healthcare_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=125000000,       # $125M endowment
            annual_payout=6500000,         # $6.5M annual spending (5.2%)
            equity_return=0.08,            # Healthcare sector returns
            bond_return=0.04,              # Standard bond returns
            equity_volatility=0.18,        # Higher healthcare volatility
            bond_volatility=0.07,          # Moderate bond volatility
            equity_allocation=0.70,        # Growth-oriented allocation
            inflation_rate=0.045,          # High healthcare inflation
            n_simulations=5000
        )
        
        # Test different healthcare inflation scenarios
        inflation_scenarios = [
            {"name": "Low Inflation", "rate": 0.030, "description": "Economic stability"},
            {"name": "Current", "rate": 0.045, "description": "Current healthcare trend"},
            {"name": "High Inflation", "rate": 0.060, "description": "Healthcare cost surge"},
            {"name": "Crisis", "rate": 0.080, "description": "Healthcare crisis scenario"}
        ]
        
        print("HEALTHCARE INFLATION IMPACT:")
        for scenario in inflation_scenarios:
            mc = EndowmentSustainabilityMonteCarlo(
                initial_value=125000000,
                annual_payout=6500000,
                equity_return=0.08,
                bond_return=0.04,
                equity_volatility=0.18,
                bond_volatility=0.07,
                equity_allocation=0.70,
                inflation_rate=scenario["rate"],
                n_simulations=3000
            )
            
            results = mc.run_simulation(years=20)
            print(f"{scenario['name']:16} ({scenario['rate']:.1%}): "
                  f"Survival {results['survival_probability']:.1%}, "
                  f"Mean Final ${results['mean_final']/1000000:.0f}M")
        
        print()
        print("PROGRAM PRIORITY ANALYSIS:")
        program_scenarios = [
            {"name": "Clinic Support", "allocation": 0.40, "inflation_adj": 1.5},
            {"name": "Medical Research", "allocation": 0.30, "inflation_adj": 1.2},
            {"name": "Community Health", "allocation": 0.20, "inflation_adj": 1.8},
            {"name": "Emergency Fund", "allocation": 0.10, "inflation_adj": 1.0}
        ]
        
        total_impact = 0
        for program in program_scenarios:
            program_impact = program["allocation"] * program["inflation_adj"]
            total_impact += program_impact
            print(f"{program['name']:18}: {program['allocation']:.0%} allocation, "
                  f"{program['inflation_adj']:.1f}x inflation multiplier")
        
        print(f"Overall Inflation Impact: {total_impact:.2f}x standard rate")
        print()
        print("RECOMMENDATIONS:")
        print("1. Reduce spending to 4.5% ($5.6M) to improve sustainability")
        print("2. Prioritize clinic support (lower inflation multiplier)")
        print("3. Create separate emergency fund for healthcare crises")
        print("4. Implement inflation-adjusted spending rules")
        print()
        
        return healthcare_mc.run_simulation(years=20)
    
    @staticmethod
    def arts_foundation_case_study():
        """
        Arts Foundation Case Study
        Organization: Metropolitan Arts Foundation
        Endowment: $45 million
        Current Spending: 6.0% annually ($2.7M)
        Mission: Support museums, theaters, arts education, public art
        Challenge: Economic sensitivity of arts funding
        """
        print("=== ARTS FOUNDATION CASE STUDY ===")
        print("Organization: Metropolitan Arts Foundation")
        print("Endowment: $45 million")
        print("Current Spending: 6.0% annually ($2.7M)")
        print("Mission: Support museums, theaters, arts education, public art")
        print("Challenge: Economic sensitivity of arts funding")
        print()
        
        # Arts foundation with economic cycle sensitivity
        arts_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=45000000,        # $45M endowment
            annual_payout=2700000,         # $2.7M annual spending (6.0%)
            equity_return=0.07,            # Conservative arts sector returns
            bond_return=0.035,             # Stable bond returns
            equity_volatility=0.20,        # High arts sector volatility
            bond_volatility=0.06,          # Low bond volatility
            equity_allocation=0.55,        # Conservative allocation
            inflation_rate=0.035,          # Standard inflation
            n_simulations=5000
        )
        
        # Economic cycle simulation
        def arts_economic_cycle_simulation(n_simulations=3000, years=20):
            cycle_results = []
            
            for sim in range(n_simulations):
                portfolio_value = 45000000
                year_values = [portfolio_value]
                
                for year in range(years):
                    # Economic cycle factor (recession every 7-10 years)
                    is_recession = (year % 8 == 0) and (np.random.random() < 0.6)
                    
                    if is_recession:
                        # Arts funding drops 30-50% during recessions
                        funding_reduction = np.random.uniform(0.30, 0.50)
                        annual_payout = 2700000 * (1 - funding_reduction)
                        
                        # Market stress during arts recessions
                        market_stress = np.random.uniform(-0.25, -0.15)
                        equity_return_sim = 0.07 + market_stress
                    else:
                        # Normal arts funding and returns
                        annual_payout = 2700000
                        equity_return_sim = np.random.normal(0.07, 0.20)
                    
                    bond_return_sim = np.random.normal(0.035, 0.06)
                    portfolio_return = 0.55 * equity_return_sim + 0.45 * bond_return_sim
                    
                    portfolio_value = portfolio_value * (1 + portfolio_return) - annual_payout
                    portfolio_value = max(portfolio_value, 0)
                    year_values.append(portfolio_value)
                
                cycle_results.append(year_values)
            
            return np.array(cycle_results)
        
        # Run economic cycle simulation
        cycle_results = arts_economic_cycle_simulation()
        cycle_survival = np.mean(cycle_results[:, -1] >= 45000000 * 0.8)
        
        print("ARTS FOUNDATION WITH ECONOMIC CYCLES:")
        print(f"Survival Probability: {cycle_survival:.1%}")
        print(f"Mean Final Value: ${np.mean(cycle_results[:, -1]):,.0f}")
        print()
        
        # Arts program resilience analysis
        arts_programs = [
            {"name": "Museums", "stability": 0.8, "recession_impact": 0.7},
            {"name": "Theaters", "stability": 0.6, "recession_impact": 0.5},
            {"name": "Arts Education", "stability": 0.9, "recession_impact": 0.8},
            {"name": "Public Art", "stability": 0.7, "recession_impact": 0.6}
        ]
        
        print("ARTS PROGRAM RESILIENCE ANALYSIS:")
        for program in arts_programs:
            resilience_score = program["stability"] * program["recession_impact"]
            print(f"{program['name']:16}: Stability {program['stability']:.1f}, "
                  f"Recession Impact {program['recession_impact']:.1f}, "
                  f"Resilience {resilience_score:.2f}")
        
        print()
        print("RECOMMENDATIONS:")
        print("1. Reduce spending to 4.5% ($2.0M) for cycle resilience")
        print("2. Prioritize arts education (highest stability)")
        print("3. Create 'crisis reserve' for recession years")
        print("4. Develop diversified funding beyond endowment")
        print()
        
        return arts_mc.run_simulation(years=20)
    
    @staticmethod
    def environmental_foundation_case_study():
        """
        Environmental Foundation Case Study
        Organization: Global Climate Action Foundation
        Endowment: $200 million
        Current Spending: 7.0% annually ($14M)
        Mission: Fund climate research, renewable energy, conservation
        Challenge: Urgent mission vs. long-term sustainability
        """
        print("=== ENVIRONMENTAL FOUNDATION CASE STUDY ===")
        print("Organization: Global Climate Action Foundation")
        print("Endowment: $200 million")
        print("Current Spending: 7.0% annually ($14M)")
        print("Mission: Fund climate research, renewable energy, conservation")
        print("Challenge: Urgent mission vs. long-term sustainability")
        print()
        
        # Environmental foundation with urgent mission needs
        climate_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=200000000,       # $200M endowment
            annual_payout=14000000,        # $14M annual spending (7.0%)
            equity_return=0.09,            # Green energy sector returns
            bond_return=0.04,              # Standard bond returns
            equity_volatility=0.22,        # High green energy volatility
            bond_volatility=0.07,          # Moderate bond volatility
            equity_allocation=0.80,        # Aggressive green energy allocation
            inflation_rate=0.040,          # Environmental project inflation
            n_simulations=5000
        )
        
        # Climate urgency vs. sustainability analysis
        urgency_scenarios = [
            {"name": "Conservative", "spending": 0.04, "climate_impact": 0.6},
            {"name": "Balanced", "spending": 0.055, "climate_impact": 0.8},
            {"name": "Urgent", "spending": 0.07, "climate_impact": 1.0},
            {"name": "Critical", "spending": 0.085, "climate_impact": 1.2}
        ]
        
        print("CLIMATE URGENCY VS SUSTAINABILITY:")
        for scenario in urgency_scenarios:
            payout = 200000000 * scenario["spending"]
            mc = EndowmentSustainabilityMonteCarlo(
                initial_value=200000000,
                annual_payout=payout,
                equity_return=0.09,
                bond_return=0.04,
                equity_volatility=0.22,
                bond_volatility=0.07,
                equity_allocation=0.80,
                inflation_rate=0.040,
                n_simulations=3000
            )
            
            results = mc.run_simulation(years=15)  # Shorter horizon for urgency
            annual_funding = payout / 1000000
            climate_score = scenario["climate_impact"] * results['survival_probability']
            
            print(f"{scenario['name']:12} ({scenario['spending']:.1%}): "
                  f"Survival {results['survival_probability']:.1%}, "
                  f"Funding ${annual_funding:.1f}M, "
                  f"Climate Score {climate_score:.2f}")
        
        print()
        print("GREEN ENERGY ALLOCATION IMPACT:")
        green_allocations = [
            {"name": "Traditional", "equity": 0.60, "green_return": 0.07},
            {"name": "Balanced", "equity": 0.75, "green_return": 0.09},
            {"name": "Green Focus", "equity": 0.85, "green_return": 0.11},
            {"name": "Aggressive Green", "equity": 0.95, "green_return": 0.13}
        ]
        
        for alloc in green_allocations:
            mc = EndowmentSustainabilityMonteCarlo(
                initial_value=200000000,
                annual_payout=14000000,
                equity_return=alloc["green_return"],
                bond_return=0.04,
                equity_volatility=0.22,
                bond_volatility=0.07,
                equity_allocation=alloc["equity"],
                inflation_rate=0.040,
                n_simulations=3000
            )
            
            results = mc.run_simulation(years=15)
            print(f"{alloc['name']:16} ({alloc['equity']:.0%} green): "
                  f"Survival {results['survival_probability']:.1%}, "
                  f"Mean Final ${results['mean_final']/1000000:.0f}M")
        
        print()
        print("RECOMMENDATIONS:")
        print("1. Adopt 5.5% spending rate ($11M) for optimal balance")
        print("2. 75% green energy allocation for mission alignment")
        print("3. Create 'climate emergency fund' for critical opportunities")
        print("4. Seek additional funding beyond endowment for climate crisis")
        print()
        
        return climate_mc.run_simulation(years=15)
    
    @staticmethod
    def american_red_cross_case_study():
        """
        American Red Cross Case Study
        Organization: American Red Cross
        Endowment: $3.4 billion
        Current Spending: 4.5% annually ($153M)
        Mission: Disaster relief, blood services, health & safety training
        Challenge: Unpredictable disaster cycles, regulatory requirements, public trust
        """
        print("=== AMERICAN RED CROSS CASE STUDY ===")
        print("Organization: American Red Cross")
        print("Endowment: $3.4 billion")
        print("Current Spending: 4.5% annually ($153M)")
        print("Mission: Disaster relief, blood services, health & safety training")
        print("Challenge: Unpredictable disaster cycles, regulatory requirements, public trust")
        print()
        
        # American Red Cross specific parameters
        arc_mc = EndowmentSustainabilityMonteCarlo(
            initial_value=3400000000,     # $3.4B endowment
            annual_payout=153000000,      # $153M annual spending (4.5%)
            equity_return=0.085,          # Historical equity return
            bond_return=0.035,            # Conservative bond return
            equity_volatility=0.18,       # Higher volatility for larger portfolio
            bond_volatility=0.06,         # Lower bond volatility
            equity_allocation=0.65,       # Current allocation
            inflation_rate=0.028,         # Recent inflation trend
            n_simulations=5000            # High accuracy for large endowment
        )
        
        # Run 30-year simulation
        results = arc_mc.run_simulation(years=30)
        
        print("BASELINE RESULTS:")
        print(f"Survival Probability (30 years): {results['survival_probability']:.2%}")
        print(f"Mean Final Value: ${results['mean_final']:,.0f}")
        print(f"Median Final Value: ${results['median_final']:,.0f}")
        print(f"5th Percentile: ${results['p5_final']:,.0f}")
        print(f"95th Percentile: ${results['p95_final']:,.0f}")
        print()
        
        # Disaster scenario modeling
        def arc_disaster_simulation(n_simulations=3000, years=30):
            """Simulate ARC endowment with unpredictable disaster years"""
            
            disaster_data = []
            
            for sim in range(n_simulations):
                portfolio_value = 3400000000
                year_values = [portfolio_value]
                
                for year in range(years):
                    # Disaster year probability (major disaster every 5-7 years)
                    is_disaster_year = np.random.random() < 0.15
                    
                    if is_disaster_year:
                        # Additional $200-500M spending during disaster years
                        disaster_spending = np.random.uniform(200000000, 500000000)
                        total_spending = 153000000 + disaster_spending
                        
                        # Market stress during disasters (reduced returns)
                        market_stress = np.random.uniform(-0.10, -0.30)
                        equity_return_sim = 0.085 + market_stress
                        bond_return_sim = 0.035 + market_stress * 0.5
                    else:
                        # Normal year spending and returns
                        total_spending = 153000000
                        equity_return_sim = np.random.normal(0.085, 0.18)
                        bond_return_sim = np.random.normal(0.035, 0.06)
                    
                    # Calculate portfolio return
                    portfolio_return = 0.65 * equity_return_sim + 0.35 * bond_return_sim
                    
                    # Update portfolio value
                    portfolio_value = portfolio_value * (1 + portfolio_return) - total_spending
                    if portfolio_value < 0:
                        portfolio_value = 0
                    
                    year_values.append(portfolio_value)
                
                disaster_data.append(year_values)
            
            return np.array(disaster_data)
        
        # Run disaster scenario analysis
        disaster_results = arc_disaster_simulation()
        disaster_survival = np.mean(disaster_results[:, -1] >= 3400000000 * 0.8)
        
        print("DISASTER SCENARIO ANALYSIS:")
        print(f"Survival with Disaster Years: {disaster_survival:.2%}")
        print(f"Mean Final Value with Disasters: ${np.mean(disaster_results[:, -1]):,.0f}")
        print(f"Impact of Disasters: {results['survival_probability'] - disaster_survival:.2%} reduction")
        print()
        
        # Allocation optimization
        print("ALLOCATION OPTIMIZATION:")
        allocation_scenarios = [
            {"name": "Conservative", "equity": 0.50, "bonds": 0.40, "alts": 0.10},
            {"name": "Current", "equity": 0.65, "bonds": 0.25, "alts": 0.10},
            {"name": "Balanced", "equity": 0.60, "bonds": 0.30, "alts": 0.10},
            {"name": "Growth", "equity": 0.75, "bonds": 0.15, "alts": 0.10}
        ]
        
        for alloc in allocation_scenarios:
            mc = EndowmentSustainabilityMonteCarlo(
                initial_value=3400000000,
                annual_payout=153000000,
                equity_return=0.085,
                bond_return=0.035,
                equity_volatility=0.18,
                bond_volatility=0.06,
                equity_allocation=alloc["equity"],
                inflation_rate=0.028,
                n_simulations=3000
            )
            
            alloc_results = mc.run_simulation(years=30)
            print(f"{alloc['name']:12} - Survival: {alloc_results['survival_probability']:.2%}, "
                  f"Mean Final: ${alloc_results['mean_final']/1e9:,.2f}B")
        
        print()
        print("STRATEGIC RECOMMENDATIONS:")
        print("1. Reduce spending rate to 4.0% ($136M annually) to improve sustainability")
        print("2. Shift to conservative allocation (50/40/10) for enhanced stability")
        print("3. Establish disaster reserve fund of $500M for catastrophic events")
        print("4. Implement quarterly Monte Carlo updates with real-time data")
        print("5. Create stakeholder communication dashboard for transparency")
        print()
        
        return results
    
    @staticmethod
    def run_all_case_studies():
        """Run all case studies and return summary results"""
        print("RUNNING ALL CASE STUDIES")
        print("=" * 50)
        print()
        
        results = {}
        
        # Run each case study
        results['university'] = CaseStudyExamples.university_endowment_case_study()
        print("-" * 50)
        results['healthcare'] = CaseStudyExamples.healthcare_foundation_case_study()
        print("-" * 50)
        results['arts'] = CaseStudyExamples.arts_foundation_case_study()
        print("-" * 50)
        results['environmental'] = CaseStudyExamples.environmental_foundation_case_study()
        print("-" * 50)
        results['american_red_cross'] = CaseStudyExamples.american_red_cross_case_study()
        
        print("=" * 50)
        print("CASE STUDY SUMMARY")
        print("=" * 50)
        
        summary_data = [
            ["Organization", "Endowment", "Current Rate", "Survival", "Recommended Rate"],
            ["University", "$850M", "4.8%", f"{results['university']['survival_probability']:.1%}", "4.5%"],
            ["Healthcare", "$125M", "5.2%", f"{results['healthcare']['survival_probability']:.1%}", "4.5%"],
            ["Arts", "$45M", "6.0%", f"{results['arts']['survival_probability']:.1%}", "4.5%"],
            ["Environmental", "$200M", "7.0%", f"{results['environmental']['survival_probability']:.1%}", "5.5%"],
            ["American Red Cross", "$3.4B", "4.5%", f"{results['american_red_cross']['survival_probability']:.1%}", "4.0%"]
        ]
        
        for row in summary_data:
            print(f"{row[0]:16} {row[1]:8} {row[2]:10} {row[3]:10} {row[4]:15}")
        
        print()
        print("KEY INSIGHTS:")
        print("- 4.5% spending rate optimal for most organizations")
        print("- Mission-specific factors significantly impact sustainability")
        print("- Economic sensitivity varies by sector")
        print("- Reserve building critical for all organizations")
        print("- Large endowments (ARC) require specialized disaster modeling")
        
        return results


# Example usage functions
def run_university_case_study():
    """Quick function to run university case study"""
    return CaseStudyExamples.university_endowment_case_study()

def run_healthcare_case_study():
    """Quick function to run healthcare case study"""
    return CaseStudyExamples.healthcare_foundation_case_study()

def run_arts_case_study():
    """Quick function to run arts case study"""
    return CaseStudyExamples.arts_foundation_case_study()

def run_environmental_case_study():
    """Quick function to run environmental case study"""
    return CaseStudyExamples.environmental_foundation_case_study()

def run_american_red_cross_case_study():
    """Quick function to run American Red Cross case study"""
    return CaseStudyExamples.american_red_cross_case_study()

def run_all_case_studies():
    """Quick function to run all case studies"""
    return CaseStudyExamples.run_all_case_studies()


if __name__ == "__main__":
    # Run all case studies
    run_all_case_studies()
