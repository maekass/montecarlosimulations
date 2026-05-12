* =============================================================================
* Stata Data Preparation for Monte Carlo Endowment Analysis
* =============================================================================
* This script prepares and formats data for comprehensive econometric analysis
* =============================================================================

clear all
set seed 12345
set more off

* =============================================================================
* 1. GENERATE COMPREHENSIVE SIMULATION DATASET
* =============================================================================

program define generate_simulation_data, rclass
    syntax, n_simulations(integer) years(integer) [output_file(string)]

    * Create master simulation dataset
    clear
    local total_obs = `n_simulations' * (`years' + 1)
    set obs `total_obs'
    
    * Generate basic identifiers
    gen simulation_id = ceil(_n / (`years' + 1))
    gen year = mod(_n - 1, `=`years' + 1')
    
    * Generate time-varying market factors
    gen equity_return = rnormal(0.08, 0.16)
    gen bond_return = rnormal(0.04, 0.08)
    gen inflation_rate = rnormal(0.03, 0.02)
    gen interest_rate = 0.02 + 0.5 * inflation_rate + rnormal(0, 0.01)
    gen market_volatility = abs(rnormal(0, 0.15))
    
    * Generate portfolio characteristics
    gen equity_allocation = 0.70
    gen initial_value = 10000000
    gen annual_payout = 315000
    
    * Simulate portfolio values
    bys simulation_id (year): gen portfolio_value = initial_value if year == 0
    
    forvalues y = 1/`years' {
        bys simulation_id: {
            replace portfolio_value = L.portfolio_value * ///
                (1 + equity_allocation * equity_return + (1 - equity_allocation) * bond_return) - ///
                annual_payout * (1 + inflation_rate) if year == `y'
            replace portfolio_value = 0 if portfolio_value < 0
        }
    }
    
    * Calculate derived variables
    gen portfolio_return = .
    bys simulation_id (year): replace portfolio_return = ///
        (portfolio_value - L.portfolio_value) / L.portfolio_value if year > 0
    
    gen log_portfolio = log(portfolio_value + 1)
    gen payout_ratio = annual_payout / L.portfolio_value if year > 0
    gen real_portfolio_value = portfolio_value / (1 + inflation_rate)^year
    
    * Generate risk indicators
    gen survived = (portfolio_value >= initial_value * 0.8)
    gen depleted = (portfolio_value == 0)
    gen drawdown = .
    bys simulation_id (year): {
        gen peak = portfolio_value[1]
        replace peak = max(peak, L.portfolio_value) if year > 0
        replace drawdown = (portfolio_value - peak) / peak if year > 0
    }
    
    * Generate scenario indicators
    gen crisis_year = (equity_return < -0.20)
    gen bull_year = (equity_return > 0.15)
    gen normal_year = !crisis_year & !bull_year
    
    * Create categorical variables
    encode normal_year, gen market_condition
    label define market_cond 0 "Crisis" 1 "Normal" 2 "Bull"
    label values market_condition market_cond
    
    * Generate lagged variables
    tsset simulation_id year
    gen L_portfolio_value = L.portfolio_value
    gen L_portfolio_return = L.portfolio_return
    gen L_market_volatility = L.market_volatility
    
    * Save dataset
    if "`output_file'" != "" {
        save "`output_file'.dta", replace
        di as txt "Dataset saved as `output_file'.dta"
    }
    
    * Summary statistics
    summarize portfolio_value portfolio_return payout_ratio drawdown
    tabulate market_condition
    tabulate survived if year == `years'
    
    return scalar n_obs = _N
    return scalar n_simulations = `n_simulations'
    return scalar years = `years'
    
end

* =============================================================================
* 2. CREATE PANEL DATA STRUCTURE
* =============================================================================

program define create_panel_structure, rclass
    syntax, input_file(string) output_file(string)

    use "`input_file'.dta", clear
    
    * Ensure proper panel structure
    xtset simulation_id year
    
    * Create panel-specific variables
    gen time_trend = year
    gen time_trend_sq = time_trend^2
    
    * Create within-transformed variables
    foreach var in portfolio_value portfolio_return payout_ratio {
        gen `var'_within = `var' - i.simulation_id
    }
    
    * Create between-transformed variables
    foreach var in portfolio_value portfolio_return payout_ratio {
        bys simulation_id: egen `var'_between = mean(`var')
    }
    
    * Create deviation from mean
    foreach var in portfolio_value portfolio_return payout_ratio {
        gen `var'_deviation = `var' - `var'_between
    }
    
    * Generate interaction terms
    gen payout_time_interact = payout_ratio * time_trend
    gen equity_time_interact = equity_allocation * time_trend
    gen volatility_time_interact = market_volatility * time_trend
    
    * Create polynomial terms
    gen payout_ratio_sq = payout_ratio^2
    gen market_volatility_sq = market_volatility^2
    
    * Save panel dataset
    save "`output_file'.dta", replace
    di as txt "Panel dataset saved as `output_file'.dta"
    
    return list
end

* =============================================================================
* 3. PREPARE TIME SERIES DATA
* =============================================================================

program define prepare_time_series, rclass
    syntax, input_file(string) output_file(string)

    use "`input_file'.dta", clear
    
    * Collapse to aggregate time series
    collapse (mean) mean_portfolio=portfolio_value ///
              mean_return=portfolio_return ///
              mean_equity=equity_return ///
              mean_bond=bond_return ///
              mean_inflation=inflation_rate ///
              mean_volatility=market_volatility ///
              (sd) sd_portfolio=portfolio_value ///
              sd_return=portfolio_return ///
              (p5) p5_portfolio=portfolio_value ///
              p25_portfolio=portfolio_value ///
              p75_portfolio=portfolio_value ///
              p95_portfolio=portfolio_value ///
              (count) n_simulations=simulation_id, by(year)
    
    * Create time series identifiers
    tsset year
    
    * Generate growth rates
    gen portfolio_growth = (mean_portfolio - L.mean_portfolio) / L.mean_portfolio
    gen return_growth = (mean_return - L.mean_return) / L.mean_return
    
    * Create moving averages
    tssmooth ma ma_portfolio = mean_portfolio, window(3)
    tssmooth ma ma_return = mean_return, window(3)
    tssmooth ma ma_volatility = mean_volatility, window(3)
    
    * Create volatility measures
    gen portfolio_volatility = sd_portfolio / mean_portfolio
    gen return_volatility = sd_return / abs(mean_return)
    
    * Create lagged variables
    gen L_mean_portfolio = L.mean_portfolio
    gen L_mean_return = L.mean_return
    gen L_mean_volatility = L.mean_volatility
    
    * Create differenced variables
    gen d_portfolio = D.mean_portfolio
    gen d_return = D.mean_return
    gen d_volatility = D.mean_volatility
    
    * Save time series dataset
    save "`output_file'.dta", replace
    di as txt "Time series dataset saved as `output_file'.dta"
    
    return list
end

* =============================================================================
* 4. PREPARE SURVIVAL DATA
* =============================================================================

program define prepare_survival_data, rclass
    syntax, input_file(string) output_file(string)

    use "`input_file'.dta", clear
    
    * Find survival times for each simulation
    preserve
    keep simulation_id year portfolio_value
    
    * Identify failure time (when portfolio drops below 80% of initial)
    gen failure_time = year if portfolio_value < 8000000 & portfolio_value[_n-1] >= 8000000
    bys simulation_id: egen time_to_failure = min(failure_time)
    
    * Create censoring indicator
    gen failed = (time_to_failure != .)
    replace time_to_failure = year if time_to_failure == . & year == 20
    
    * Create baseline covariates
    gen initial_value = 10000000
    gen payout_ratio = 315000 / initial_value
    gen equity_allocation = 0.70
    gen log_initial = log(initial_value)
    
    * Create time-varying covariates at baseline
    bys simulation_id: keep if _n == 1
    
    * Generate additional covariates
    gen high_payout = (payout_ratio > 0.04)
    gen aggressive_allocation = (equity_allocation > 0.6)
    
    * Save survival dataset
    save "`output_file'.dta", replace
    di as txt "Survival dataset saved as `output_file'.dta"
    
    * Summary statistics
    summarize time_to_failure
    tabulate failed
    tabulate high_payout failed, row
    tabulate aggressive_allocation failed, row
    
    restore
    return list
end

* =============================================================================
* 5. CREATE CROSS-SECTIONAL DATASET
* =============================================================================

program define create_cross_sectional, rclass
    syntax, input_file(string) output_file(string)

    use "`input_file'.dta", clear
    
    * Create cross-sectional dataset (final year observations)
    keep if year == 20
    
    * Generate outcome variables
    gen final_portfolio_value = portfolio_value
    gen total_return = (final_portfolio_value - 10000000) / 10000000
    gen log_final_value = log(final_portfolio_value + 1)
    
    * Generate risk measures
    gen max_drawdown = .
    gen volatility = .
    gen sharpe_ratio = .
    
    * Calculate risk metrics for each simulation
    preserve
    keep simulation_id year portfolio_value portfolio_return
    bys simulation_id (year): {
        gen peak = portfolio_value[1]
        replace peak = max(peak, portfolio_value) if year > 0
        gen drawdown = (portfolio_value - peak) / peak
        replace max_drawdown = min(drawdown) if _n == _N
        replace volatility = sd(portfolio_return) if _n == _N
        gen excess_return = portfolio_return - 0.02  // Risk-free rate = 2%
        replace sharpe_ratio = mean(excess_return) / volatility if _n == _N
    }
    keep if year == 20
    keep simulation_id max_drawdown volatility sharpe_ratio
    tempfile risk_metrics
    save `risk_metrics'
    restore
    
    * Merge risk metrics
    merge 1:1 simulation_id using `risk_metrics'
    
    * Generate additional covariates
    gen payout_ratio = 315000 / 10000000
    gen equity_allocation = 0.70
    gen log_initial = log(10000000)
    
    * Create interaction terms
    gen payout_equity_interact = payout_ratio * equity_allocation
    gen payout_volatility_interact = payout_ratio * volatility
    
    * Create categorical variables
    gen high_performance = (total_return > 0.5)
    gen low_risk = (volatility < 0.15)
    gen sustainable = (final_portfolio_value >= 8000000)
    
    * Save cross-sectional dataset
    save "`output_file'.dta", replace
    di as txt "Cross-sectional dataset saved as `output_file'.dta"
    
    * Summary statistics
    summarize final_portfolio_value total_return volatility sharpe_ratio
    tabulate sustainable
    tabulate high_performance low_risk
    
    return list
end

* =============================================================================
* 6. VALIDATION AND QUALITY CHECKS
* =============================================================================

program define validate_data, rclass
    syntax, input_file(string)

    use "`input_file'.dta", clear
    
    di as txt "=== DATA VALIDATION REPORT ==="
    
    * Check for missing values
    foreach var in simulation_id year portfolio_value {
        count if missing(`var')
        di as result "Missing values in `var': " r(N)
    }
    
    * Check for duplicates
    duplicates report simulation_id year
    duplicates drop simulation_id year, force
    di as result "Duplicates removed"
    
    * Check for impossible values
    count if portfolio_value < 0
    di as result "Negative portfolio values: " r(N)
    
    count if year < 0 | year > 20
    di as result "Invalid years: " r(N)
    
    * Check data consistency
    bys simulation_id: gen obs_per_sim = _N
    summarize obs_per_sim
    di as result "Observations per simulation: " r(mean) " (should be 21)"
    
    * Check for outliers
    summarize portfolio_value
    gen outlier = (portfolio_value > r(p99) | portfolio_value < r(p1))
    count if outlier
    di as result "Outliers in portfolio value: " r(N)
    
    * Generate data quality report
    gen data_quality = 1
    replace data_quality = 0 if missing(portfolio_value)
    replace data_quality = 0 if portfolio_value < 0
    replace data_quality = 0 if outlier
    
    summarize data_quality
    di as result "Data quality score: " r(mean)
    
    return scalar data_quality = r(mean)
    return scalar n_outliers = r(N) if outlier
    return scalar n_missing = r(N) if missing(portfolio_value)
    
end

* =============================================================================
* 7. EXPORT DATA FOR EXTERNAL ANALYSIS
* =============================================================================

program define export_for_analysis, rclass
    syntax, input_file(string) export_format(string)

    use "`input_file'.dta", clear
    
    if "`export_format'" == "csv" {
        export delimited "monte_carlo_data.csv", replace
        di as txt "Data exported to monte_carlo_data.csv"
    }
    else if "`export_format'" == "excel" {
        export excel "monte_carlo_data.xlsx", firstrow(variables) replace
        di as txt "Data exported to monte_carlo_data.xlsx"
    }
    else if "`export_format'" == "stata" {
        save "monte_carlo_data_final.dta", replace
        di as txt "Data saved as monte_carlo_data_final.dta"
    }
    else if "`export_format'" == "r" {
        * Export for R analysis
        export delimited "monte_carlo_data.csv", replace
        di as txt "Data exported for R analysis"
    }
    else if "`export_format'" == "python" {
        * Export for Python analysis
        export delimited "monte_carlo_data.csv", replace
        di as txt "Data exported for Python analysis"
    }
    else {
        di as error "Invalid export format. Use csv, excel, stata, r, or python"
    }
    
    return list
end

* =============================================================================
* 8. MAIN EXECUTION
* =============================================================================

di as txt "=== STATA DATA PREPARATION FOR MONTE CARLO ANALYSIS ==="
di as txt "Preparing comprehensive datasets..." _newline

* 1. Generate base simulation data
di as txt "1. Generating base simulation data"
generate_simulation_data, n_simulations(1000) years(20) output_file("base_simulation")
di as result "Base simulation data generated" _newline

* 2. Create panel structure
di as txt "2. Creating panel data structure"
create_panel_structure, input_file("base_simulation") output_file("panel_data")
di as result "Panel data structure created" _newline

* 3. Prepare time series data
di as txt "3. Preparing time series data"
prepare_time_series, input_file("base_simulation") output_file("time_series")
di as result "Time series data prepared" _newline

* 4. Prepare survival data
di as txt "4. Preparing survival data"
prepare_survival_data, input_file("base_simulation") output_file("survival_data")
di as result "Survival data prepared" _newline

* 5. Create cross-sectional data
di as txt "5. Creating cross-sectional data"
create_cross_sectional, input_file("base_simulation") output_file("cross_sectional")
di as result "Cross-sectional data created" _newline

* 6. Validate data
di as txt "6. Validating data quality"
validate_data, input_file("base_simulation")
di as result "Data validation completed" _newline

* 7. Export for analysis
di as txt "7. Exporting data for external analysis"
export_for_analysis, input_file("base_simulation") export_format("excel")
export_for_analysis, input_file("base_simulation") export_format("csv")
di as result "Data exported in multiple formats" _newline

di as txt "=== DATA PREPARATION COMPLETE ==="
di as txt "Datasets created:"
di as txt "- base_simulation.dta"
di as txt "- panel_data.dta"
di as txt "- time_series.dta"
di as txt "- survival_data.dta"
di as txt "- cross_sectional.dta"
di as txt "- monte_carlo_data.xlsx"
di as txt "- monte_carlo_data.csv"
di as txt ""
di as txt "Ready for advanced econometric analysis!"

* End of data preparation script
