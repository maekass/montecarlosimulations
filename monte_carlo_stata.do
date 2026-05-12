* =============================================================================
* Monte Carlo Simulations for Non-Profit Endowments - Stata Implementation
* =============================================================================
* This Stata do-file implements comprehensive Monte Carlo simulations with
* advanced econometric analysis for non-profit endowment management
* =============================================================================

clear all
set seed 12345
set more off
set matsize 1000

* =============================================================================
* GLOBAL PARAMETERS
* =============================================================================
global initial_value = 10000000
global annual_payout = 315000
global equity_return = 0.08
global bond_return = 0.04
global equity_volatility = 0.16
global bond_volatility = 0.08
global equity_allocation = 0.70
global inflation_rate = 0.03
global time_horizon = 20
global n_simulations = 1000

* =============================================================================
* 1. MONTE CARLO SIMULATION - ENDOVEMENT SUSTAINABILITY
* =============================================================================

program define monte_carlo_endowment, rclass
    syntax, n_simulations(integer) years(integer) [ ///
        initial_value(real 10000000) ///
        annual_payout(real 315000) ///
        equity_return(real 0.08) ///
        bond_return(real 0.04) ///
        equity_volatility(real 0.16) ///
        bond_volatility(real 0.08) ///
        equity_allocation(real 0.70) ///
        inflation_rate(real 0.03) ///
    ]

    * Create simulation dataset
    clear
    set obs `=`years' + 1'
    gen year = _n - 1
    
    * Initialize results matrix
    matrix results = J(`n_simulations', `=`years' + 1', .)
    
    * Run simulations
    forvalues i = 1/`n_simulations' {
        * Initialize portfolio value
        scalar portfolio_value = `initial_value'
        results[`i', 1] = portfolio_value
        
        * Simulate each year
        forvalues y = 1/`years' {
            * Generate random returns
            scalar equity_return_sim = rnormal(`equity_return', `equity_volatility')
            scalar bond_return_sim = rnormal(`bond_return', `bond_volatility')
            
            * Calculate portfolio return
            scalar portfolio_return = `equity_allocation' * equity_return_sim + ///
                                    (1 - `equity_allocation') * bond_return_sim
            
            * Update portfolio value
            scalar portfolio_value = portfolio_value * (1 + portfolio_return) - `annual_payout'
            
            * Ensure non-negative
            if portfolio_value < 0 {
                scalar portfolio_value = 0
            }
            
            * Store result
            results[`i', `=`y' + 1'] = portfolio_value
        }
    }
    
    * Convert matrix to dataset
    clear
    svmat results, names(sim)
    gen simulation_id = _n
    
    * Reshape to long format
    reshape long sim, i(simulation_id) j(year)
    rename sim portfolio_value
    
    * Calculate summary statistics
    replace portfolio_value = round(portfolio_value, 0.01)
    
    * Return results
    return scalar survival_prob = mean(portfolio_value >= `initial_value' * 0.8) if year == `years'
    return scalar mean_final = mean(portfolio_value) if year == `years'
    return scalar median_final = median(portfolio_value) if year == `years'
    return scalar p5_final = _pctile[5] if year == `years'
    return scalar p95_final = _pctile[95] if year == `years'
    
end

* =============================================================================
* 2. WITHDRAWAL STRATEGY COMPARISON
* =============================================================================

program define withdrawal_strategy_comparison, rclass
    syntax, n_simulations(integer) years(integer) ///
        fixed_amount(real 315000) percentage_rate(real 0.05)

    * Fixed strategy simulation
    monte_carlo_endowment, n_simulations(`n_simulations') years(`years') ///
        annual_payout(`fixed_amount')
    preserve
    keep if year == `years'
    gen strategy = "Fixed"
    gen strategy_type = "fixed"
    gen annual_payout = `fixed_amount'
    tempfile fixed_results
    save `fixed_results'
    restore

    * Percentage strategy simulation
    clear
    set obs `=`years' + 1'
    gen year = _n - 1
    matrix perc_results = J(`n_simulations', `=`years' + 1', .)
    
    forvalues i = 1/`n_simulations' {
        scalar portfolio_value = $initial_value
        perc_results[`i', 1] = portfolio_value
        
        forvalues y = 1/`years' {
            * Calculate percentage payout
            scalar payout = portfolio_value * `percentage_rate'
            
            * Generate returns
            scalar equity_return_sim = rnormal($equity_return, $equity_volatility)
            scalar bond_return_sim = rnormal($bond_return, $bond_volatility)
            scalar portfolio_return = $equity_allocation * equity_return_sim + ///
                                    (1 - $equity_allocation) * bond_return_sim
            
            * Update portfolio
            scalar portfolio_value = portfolio_value * (1 + portfolio_return) - payout
            if portfolio_value < 0 {
                scalar portfolio_value = 0
            }
            
            perc_results[`i', `=`y' + 1'] = portfolio_value
        }
    }
    
    * Convert to dataset
    clear
    svmat perc_results, names(sim)
    gen simulation_id = _n
    reshape long sim, i(simulation_id) j(year)
    rename sim portfolio_value
    gen strategy = "Percentage"
    gen strategy_type = "percentage"
    gen annual_payout = .
    replace annual_payout = portfolio_value * `percentage_rate' if year < `years'
    
    * Combine results
    append using `fixed_results'
    
    * Calculate survival rates
    gen survived = (portfolio_value >= $initial_value * 0.8) if year == `years'
    
    * Return results
    collapse (mean) survived portfolio_value, by(strategy strategy_type)
    rename survived survival_rate
    rename portfolio_value mean_final_value
    
    return list
end

* =============================================================================
* 3. ASSET ALLOCATION TESTING
* =============================================================================

program define asset_allocation_test, rclass
    syntax, n_simulations(integer) years(integer)

    * Define allocation strategies
    matrix allocations = (0.30, 0.70 \  /// Conservative
                         0.60, 0.40 \  /// Balanced
                         0.70, 0.30 \  /// Aggressive
                         0.90, 0.10)   /// Very Aggressive
    
    local strategies "Conservative Balanced Aggressive Very_Aggressive"
    
    * Initialize results storage
    clear
    gen strategy = ""
    gen equity_allocation = .
    gen bond_allocation = .
    gen survival_rate = .
    gen mean_final_value = .
    gen volatility = .
    gen sharpe_ratio = .
    
    local row = 1
    
    * Test each allocation
    forvalues i = 1/4 {
        local strategy : word `i' of `strategies'
        scalar equity_alloc = allocations[`i', 1]
        scalar bond_alloc = allocations[`i', 2]
        
        * Run simulation
        monte_carlo_endowment, n_simulations(`n_simulations') years(`years') ///
            equity_allocation(`equity_alloc')
        
        * Calculate statistics
        preserve
        keep if year == `years'
        gen returns = (portfolio_value - $initial_value) / $initial_value
        gen survived = (portfolio_value >= $initial_value * 0.8)
        
        * Calculate Sharpe ratio (assuming risk-free rate = 2%)
        scalar risk_free = 0.02
        scalar excess_return = mean(returns) - risk_free
        scalar return_std = sd(returns)
        scalar sharpe = excess_return / return_std
        
        * Store results
        replace strategy = "`strategy'" in `row'
        replace equity_allocation = `equity_alloc' in `row'
        replace bond_allocation = `bond_alloc' in `row'
        replace survival_rate = mean(survived) in `row'
        replace mean_final_value = mean(portfolio_value) in `row'
        replace volatility = sd(returns) in `row'
        replace sharpe_ratio = `sharpe' in `row'
        
        local ++row
        restore
    }
    
    * Display results
    list strategy equity_allocation survival_rate mean_final_value volatility sharpe_ratio, ///
        clean noobs
    
    return list
end

* =============================================================================
* 4. CRISIS MANAGEMENT SIMULATION
* =============================================================================

program define crisis_management, rclass
    syntax, n_simulations(integer) years(integer) ///
        crisis_probability(real 0.05) crisis_drop(real -0.30)

    * Create simulation dataset
    clear
    set obs `=`years' + 1'
    gen year = _n - 1
    
    matrix crisis_results = J(`n_simulations', `=`years' + 1', .)
    matrix crisis_indicators = J(`n_simulations', `=`years' + 1', .)
    
    * Run crisis simulations
    forvalues i = 1/`n_simulations' {
        scalar portfolio_value = $initial_value
        crisis_results[`i', 1] = portfolio_value
        crisis_indicators[`i', 1] = 0
        
        forvalues y = 1/`years' {
            * Check if crisis occurs
            scalar is_crisis = (runiform() < `crisis_probability')
            
            if is_crisis {
                scalar portfolio_return = `crisis_drop'
                crisis_indicators[`i', `=`y' + 1'] = 1
            }
            else {
                scalar equity_return_sim = rnormal($equity_return, $equity_volatility)
                scalar bond_return_sim = rnormal($bond_return, $bond_volatility)
                scalar portfolio_return = $equity_allocation * equity_return_sim + ///
                                        (1 - $equity_allocation) * bond_return_sim
                crisis_indicators[`i', `=`y' + 1'] = 0
            }
            
            * Update portfolio
            scalar portfolio_value = portfolio_value * (1 + portfolio_return) - $annual_payout
            if portfolio_value < 0 {
                scalar portfolio_value = 0
            }
            
            crisis_results[`i', `=`y' + 1'] = portfolio_value
        }
    }
    
    * Convert to dataset
    clear
    svmat crisis_results, names(portfolio)
    svmat crisis_indicators, names(crisis)
    gen simulation_id = _n
    reshape long portfolio crisis, i(simulation_id) j(year)
    rename portfolio portfolio_value
    
    * Calculate survival rate
    gen survived = (portfolio_value >= $initial_value * 0.8) if year == `years'
    
    * Return results
    summarize survived if year == `years'
    return scalar survival_rate = r(mean)
    
    summarize portfolio_value if year == `years'
    return scalar mean_final = r(mean)
    return scalar std_final = r(sd)
end

* =============================================================================
* 5. ADVANCED ECONOMETRIC ANALYSIS
* =============================================================================

* Panel Data Analysis of Simulation Results
program define panel_data_analysis
    syntax, n_simulations(integer) years(integer)

    * Generate panel data
    monte_carlo_endowment, n_simulations(`n_simulations') years(`years')
    
    * Create panel identifiers
    xtset simulation_id year
    
    * Calculate growth rates
    gen growth_rate = (portfolio_value - L.portfolio_value) / L.portfolio_value if year > 0
    
    * Panel regression with fixed effects
    xtreg portfolio_value year, fe
    estimates store fixed_effects
    
    * Random effects model
    xtreg portfolio_value year, re
    estimates store random_effects
    
    * Hausman test
    hausman fixed_effects random_effects
    
    * Dynamic panel model (Arellano-Bond)
    xtset simulation_id year
    xtabond portfolio_value L.portfolio_year, lags(1)
    
end

* Time Series Analysis of Aggregate Results
program define time_series_analysis
    syntax, n_simulations(integer) years(integer)

    * Generate simulation data
    monte_carlo_endowment, n_simulations(`n_simulations') years(`years')
    
    * Calculate aggregate statistics by year
    collapse (mean) mean_portfolio=portfolio_value ///
              (sd) sd_portfolio=portfolio_value ///
              (p5) p5_portfolio=portfolio_value ///
              (p95) p95_portfolio=portfolio_value, by(year)
    
    * Time series plot setup
    tsset year
    
    * ARIMA model for mean portfolio value
    arima mean_portfolio, arima(1,1,1)
    estimates store arima_model
    
    * Forecast next 5 years
    tsappend, add(5)
    predict forecast_mean, dynamic(`=`years'')
    
    * GARCH model for volatility
    arch sd_portfolio, arch(1) garch(1)
    estimates store garch_model
    
end

* Survival Analysis
program define survival_analysis
    syntax, n_simulations(integer) years(integer)

    * Generate simulation data
    monte_carlo_endowment, n_simulations(`n_simulations') years(`years')
    
    * Create survival data
    preserve
    keep simulation_id year portfolio_value
    
    * Find depletion year for each simulation
    bys simulation_id (year): gen depletion_year = year if portfolio_value == 0 & portfolio_value[_n-1] > 0
    bys simulation_id: egen first_depletion = min(depletion_year)
    
    * Create survival time variable
    gen survival_time = first_depletion if first_depletion != .
    replace survival_time = `years' + 1 if first_depletion == .
    gen failed = (first_depletion != .)
    
    * Keep one observation per simulation
    bys simulation_id: keep if _n == 1
    
    * Kaplan-Meier survival estimator
    stset survival_time, failure(failed)
    sts graph, title("Endowment Survival Curve") ///
           ytitle("Survival Probability") xtitle("Years")
    
    * Cox proportional hazards model
    * Create covariates (would need additional simulation parameters)
    gen initial_value_log = log($initial_value)
    gen payout_ratio = $annual_payout / $initial_value
    
    stcox initial_value_log payout_ratio
    estimates store cox_model
    
    restore
end

* =============================================================================
* 6. BAYESIAN MONTE CARLO
* =============================================================================

program define bayesian_monte_carlo, rclass
    syntax, n_simulations(integer) years(integer) n_draws(integer 1000)

    * Define prior distributions
    * Equity return prior: Normal(0.08, 0.02)
    * Bond return prior: Normal(0.04, 0.01)
    * Equity volatility prior: Gamma(2, 0.08)
    * Bond volatility prior: Gamma(2, 0.04)
    
    matrix posterior_results = J(`n_draws', 5, .)
    
    * Bayesian inference loop
    forvalues d = 1/`n_draws' {
        * Draw from priors
        scalar equity_return_draw = rnormal(0.08, 0.02)
        scalar bond_return_draw = rnormal(0.04, 0.01)
        scalar equity_vol_draw = rgamma(2, 0.08)
        scalar bond_vol_draw = rgamma(2, 0.04)
        
        * Run Monte Carlo with drawn parameters
        monte_carlo_endowment, n_simulations(`n_simulations') years(`years') ///
            equity_return(`equity_return_draw') ///
            bond_return(`bond_return_draw') ///
            equity_volatility(`equity_vol_draw') ///
            bond_volatility(`bond_vol_draw')
        
        * Store posterior results
        preserve
        keep if year == `years'
        posterior_results[`d', 1] = equity_return_draw
        posterior_results[`d', 2] = bond_return_draw
        posterior_results[`d', 3] = equity_vol_draw
        posterior_results[`d', 4] = mean(portfolio_value)
        posterior_results[`d', 5] = mean(portfolio_value >= $initial_value * 0.8)
        restore
    }
    
    * Convert to dataset for analysis
    clear
    svmat posterior_results, names(eq_return bd_return eq_vol final_value survival)
    
    * Summarize posterior distributions
    summarize eq_return bd_return eq_vol final_value survival
    
    * Calculate credible intervals
    foreach var in eq_return bd_return eq_vol final_value survival {
        centile `var', centile(2.5 50 97.5)
    }
    
end

* =============================================================================
* 7. MAIN EXECUTION
* =============================================================================

* Run all simulations and analyses
di as txt "=== MONTE CARLO SIMULATIONS FOR NON-PROFIT ENDOWMENTS ==="
di as txt "Running comprehensive analysis..." _newline

* 1. Basic sustainability analysis
di as txt "1. Endowment Sustainability Analysis"
monte_carlo_endowment, n_simulations($n_simulations) years($time_horizon)
di as result "Survival Probability: " %4.2f r(survival_prob)
di as result "Mean Final Value: $" %12.0fc r(mean_final)
di as result "Median Final Value: $" %12.0fc r(median_final)
di as result "5th Percentile: $" %12.0fc r(p5_final)
di as result "95th Percentile: $" %12.0fc r(p95_final) _newline

* 2. Withdrawal strategy comparison
di as txt "2. Withdrawal Strategy Comparison"
withdrawal_strategy_comparison, n_simulations($n_simulations) years($time_horizon) ///
    fixed_amount($annual_payout) percentage_rate(0.05)
list, clean noobs _newline

* 3. Asset allocation testing
di as txt "3. Asset Allocation Testing"
asset_allocation_test, n_simulations($n_simulations) years($time_horizon) _newline

* 4. Crisis management
di as txt "4. Crisis Management Analysis"
crisis_management, n_simulations($n_simulations) years($time_horizon) ///
    crisis_probability(0.05) crisis_drop(-0.30)
di as result "Crisis Survival Rate: " %4.2f r(survival_rate)
di as result "Mean Final Value: $" %12.0fc r(mean_final) _newline

* 5. Advanced econometric analysis
di as txt "5. Advanced Econometric Analysis"
panel_data_analysis, n_simulations(500) years($time_horizon)
time_series_analysis, n_simulations($n_simulations) years($time_horizon)
survival_analysis, n_simulations($n_simulations) years($time_horizon) _newline

* 6. Bayesian analysis
di as txt "6. Bayesian Monte Carlo Analysis"
bayesian_monte_carlo, n_simulations(500) years($time_horizon) n_draws(1000)

di as txt "=== ANALYSIS COMPLETE ==="
di as txt "Results saved in memory and can be exported to Excel/CSV"

* =============================================================================
* 8. EXPORT RESULTS
* =============================================================================

* Export to Excel
program define export_results
    syntax, filename(string)

    * Create summary dataset
    clear
    gen analysis = ""
    gen metric = ""
    gen value = .
    
    local row = 1
    
    * Basic results
    monte_carlo_endowment, n_simulations($n_simulations) years($time_horizon)
    set obs `=`row' + 4'
    replace analysis = "Sustainability" in `=`row'/`=`row'+4'
    replace metric = "Survival Probability" in `row'
    replace metric = "Mean Final Value" in `=`row'+1'
    replace metric = "Median Final Value" in `=`row'+2'
    replace metric = "5th Percentile" in `=`row'+3'
    replace metric = "95th Percentile" in `=`row'+4'
    replace value = r(survival_prob) in `row'
    replace value = r(mean_final) in `=`row'+1'
    replace value = r(median_final) in `=`row'+2'
    replace value = r(p5_final) in `=`row'+3'
    replace value = r(p95_final) in `=`row'+4'
    
    * Export to Excel
    export excel "`filename'.xlsx", firstrow(variables) replace
    
    di as txt "Results exported to `filename'.xlsx"
end

* Export results
export_results, filename("monte_carlo_results")

* End of program
