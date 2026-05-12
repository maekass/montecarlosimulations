-- Monte Carlo Simulations for Non-Profit Endowments - SQL Implementation
-- This SQL implementation demonstrates Monte Carlo simulation using PostgreSQL
-- Suitable for database-backed simulation and analysis

-- Table structure for storing simulation parameters
CREATE TABLE IF NOT EXISTS simulation_parameters (
    id SERIAL PRIMARY KEY,
    parameter_name VARCHAR(100),
    parameter_value DECIMAL(20, 6),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for storing simulation results
CREATE TABLE IF NOT EXISTS simulation_results (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER,
    iteration INTEGER,
    year INTEGER,
    portfolio_value DECIMAL(20, 2),
    equity_return DECIMAL(10, 6),
    bond_return DECIMAL(10, 6),
    scenario_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for storing endowment parameters
CREATE TABLE IF NOT EXISTS endowment_parameters (
    id SERIAL PRIMARY KEY,
    initial_value DECIMAL(20, 2),
    annual_payout DECIMAL(20, 2),
    equity_allocation DECIMAL(5, 4),
    equity_return_mean DECIMAL(10, 6),
    equity_return_std DECIMAL(10, 6),
    bond_return_mean DECIMAL(10, 6),
    bond_return_std DECIMAL(10, 6),
    inflation_rate DECIMAL(10, 6),
    time_horizon INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to generate random normal distribution (Box-Muller transform)
CREATE OR REPLACE FUNCTION random_normal(mean DECIMAL, std_dev DECIMAL)
RETURNS DECIMAL AS $$
DECLARE
    u1 DECIMAL;
    u2 DECIMAL;
    z0 DECIMAL;
    result DECIMAL;
BEGIN
    u1 := RANDOM()::DECIMAL / 2147483647.0;
    u2 := RANDOM()::DECIMAL / 2147483647;
    z0 := SQRT(-2.0 * LN(u1)) * COS(2.0 * 3.14159265359 * u2);
    result := mean + std_dev * z0;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to run Monte Carlo simulation for endowment
CREATE OR REPLACE FUNCTION run_endowment_monte_carlo(
    p_n_simulations INTEGER,
    p_years INTEGER
)
RETURNS TABLE (
    iteration INTEGER,
    year INTEGER,
    portfolio_value DECIMAL,
    equity_return DECIMAL,
    bond_return DECIMAL
) AS $$
DECLARE
    v_initial_value DECIMAL;
    v_annual_payout DECIMAL;
    v_equity_allocation DECIMAL;
    v_equity_return_mean DECIMAL;
    v_equity_return_std DECIMAL;
    v_bond_return_mean DECIMAL;
    v_bond_return_std DECIMAL;
    v_inflation_rate DECIMAL;
    i INTEGER;
    y INTEGER;
    v_portfolio_value DECIMAL;
    v_equity_return DECIMAL;
    v_bond_return DECIMAL;
    v_portfolio_return DECIMAL;
    v_inflation_adjusted_payout DECIMAL;
BEGIN
    -- Get endowment parameters
    SELECT 
        initial_value, 
        annual_payout, 
        equity_allocation,
        equity_return_mean,
        equity_return_std,
        bond_return_mean,
        bond_return_std,
        inflation_rate
    INTO 
        v_initial_value,
        v_annual_payout,
        v_equity_allocation,
        v_equity_return_mean,
        v_equity_return_std,
        v_bond_return_mean,
        v_bond_return_std,
        v_inflation_rate
    FROM endowment_parameters
    ORDER BY created_at DESC
    LIMIT 1;
    
    -- Run simulations
    FOR i IN 1..p_n_simulations LOOP
        v_portfolio_value := v_initial_value;
        
        FOR y IN 0..p_years LOOP
            RETURN QUERY SELECT 
                i, 
                y, 
                v_portfolio_value,
                0.0, -- equity_return
                0.0  -- bond_return;
            
            IF y < p_years THEN
                -- Generate random returns
                v_equity_return := random_normal(v_equity_return_mean, v_equity_return_std);
                v_bond_return := random_normal(v_bond_return_mean, v_bond_return_std);
                
                -- Calculate portfolio return
                v_portfolio_return := (v_equity_allocation * v_equity_return + 
                                      (1 - v_equity_allocation) * v_bond_return);
                
                -- Apply return
                v_portfolio_value := v_portfolio_value * (1 + v_portfolio_return);
                
                -- Apply inflation-adjusted payout
                v_inflation_adjusted_payout := v_annual_payout * POWER(1 + v_inflation_rate, y);
                v_portfolio_value := v_portfolio_value - v_inflation_adjusted_payout;
                
                -- Ensure non-negative
                IF v_portfolio_value < 0 THEN
                    v_portfolio_value := 0;
                END IF;
            END IF;
        END LOOP;
    END LOOP;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate survival probability
CREATE OR REPLACE FUNCTION calculate_survival_probability(
    p_threshold_percentage DECIMAL
)
RETURNS DECIMAL AS $$
DECLARE
    v_total_simulations INTEGER;
    v_surviving_simulations INTEGER;
    v_survival_probability DECIMAL;
BEGIN
    SELECT COUNT(DISTINCT iteration) INTO v_total_simulations
    FROM simulation_results
    WHERE year = (SELECT MAX(year) FROM simulation_results);
    
    SELECT COUNT(DISTINCT iteration) INTO v_surviving_simulations
    FROM simulation_results
    WHERE year = (SELECT MAX(year) FROM simulation_results)
    AND portfolio_value >= (SELECT initial_value * p_threshold_percentage FROM endowment_parameters ORDER BY created_at DESC LIMIT 1);
    
    v_survival_probability := (v_surviving_simulations::DECIMAL / v_total_simulations::DECIMAL) * 100;
    
    RETURN v_survival_probability;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate percentile statistics
CREATE OR REPLACE FUNCTION calculate_percentile_statistics()
RETURNS TABLE (
    percentile_5 DECIMAL,
    percentile_25 DECIMAL,
    percentile_50 DECIMAL,
    percentile_75 DECIMAL,
    percentile_95 DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY portfolio_value),
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY portfolio_value),
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY portfolio_value),
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY portfolio_value),
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY portfolio_value)
    FROM simulation_results
    WHERE year = (SELECT MAX(year) FROM simulation_results);
END;
$$ LANGUAGE plpgsql;

-- Example usage: Insert endowment parameters
INSERT INTO endowment_parameters (
    initial_value, annual_payout, equity_allocation,
    equity_return_mean, equity_return_std,
    bond_return_mean, bond_return_std,
    inflation_rate, time_horizon
) VALUES (
    10000000.00,  -- $10M initial value
    315000.00,   -- $315K annual payout
    0.70,        -- 70% equity allocation
    0.08,        -- 8% equity return mean
    0.16,        -- 16% equity return std
    0.04,        -- 4% bond return mean
    0.08,        -- 8% bond return std
    0.03,        -- 3% inflation rate
    20           -- 20 year horizon
);

-- Example usage: Run Monte Carlo simulation (1000 iterations, 20 years)
-- SELECT * FROM run_endowment_monte_carlo(1000, 20);

-- Example usage: Calculate survival probability (80% threshold)
-- SELECT calculate_survival_probability(0.80);

-- Example usage: Calculate percentile statistics
-- SELECT * FROM calculate_percentile_statistics();

-- View for quick statistics
CREATE OR REPLACE VIEW endowment_statistics AS
SELECT 
    year,
    COUNT(DISTINCT iteration) as total_simulations,
    AVG(portfolio_value) as mean_value,
    STDDEV(portfolio_value) as std_value,
    MIN(portfolio_value) as min_value,
    MAX(portfolio_value) as max_value,
    PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY portfolio_value) as percentile_5,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY portfolio_value) as percentile_95
FROM simulation_results
GROUP BY year
ORDER BY year;
