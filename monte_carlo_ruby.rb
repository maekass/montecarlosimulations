# Monte Carlo Simulations for Non-Profit Endowments - Ruby Implementation
# Ruby implementation for Monte Carlo simulations with clean, idiomatic code

require 'matrix'

# Set random seed for reproducibility
srand(42)

# Base module for Monte Carlo simulations
module MonteCarlo
  # Utility class for random number generation
  class RandomGenerator
    def self.normal(mean: 0, std: 1)
      # Box-Muller transform
      u1 = rand
      u2 = rand
      z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math::PI * u2)
      mean + std * z0
    end

    def self.gamma(shape: 2, scale: 1)
      # Simple gamma approximation
      sum = 0
      shape.to_i.times { sum += -Math.log(rand) }
      sum * scale
    end
  end

  # Portfolio simulation using Geometric Brownian Motion
  class PortfolioSimulation
    attr_reader :returns, :volatility, :initial_investment, :n_simulations

    def initialize(returns:, volatility:, initial_investment:, n_simulations: 10000)
      @returns = returns
      @volatility = volatility
      @initial_investment = initial_investment
      @n_simulations = n_simulations
    end

    def simulate(time_horizon: 252)
      dt = 1.0 / time_horizon
      daily_returns = Array.new(@n_simulations) { Array.new(time_horizon) }

      (0...@n_simulations).each do |i|
        (0...time_horizon).each do |j|
          z = RandomGenerator.normal
          daily_returns[i][j] = (@returns - 0.5 * @volatility**2) * dt + 
                                @volatility * Math.sqrt(dt) * z
        end
      end

      # Calculate cumulative returns
      portfolio_values = Array.new(@n_simulations) { Array.new(time_horizon + 1, @initial_investment) }
      
      (0...@n_simulations).each do |i|
        (1...time_horizon + 1).each do |j|
          portfolio_values[i][j] = portfolio_values[i][j - 1] * (1 + daily_returns[i][j - 1])
        end
      end

      portfolio_values
    end

    def run(time_horizon: 252)
      values = simulate(time_horizon: time_horizon)
      final_values = values.map { |v| v.last }

      {
        final_values: final_values,
        mean: final_values.sum / final_values.size.to_f,
        median: final_values.sort[final_values.size / 2],
        std: Math.sqrt(final_values.map { |x| (x - mean) ** 2 }.sum / final_values.size.to_f),
        percentile_5: final_values.sort[(final_values.size * 0.05).to_i],
        percentile_95: final_values.sort[(final_values.size * 0.95).to_i],
        all_paths: values
      }
    end
  end

  # Endowment sustainability simulation
  class EndowmentSustainability
    attr_reader :initial_value, :annual_payout, :equity_return, :bond_return,
                :equity_volatility, :bond_volatility, :equity_allocation,
                :inflation_rate, :n_simulations

    def initialize(initial_value:, annual_payout:, equity_return:, bond_return,
                   equity_volatility:, bond_volatility:, equity_allocation: 0.7,
                   inflation_rate: 0.03, n_simulations: 10000)
      @initial_value = initial_value
      @annual_payout = annual_payout
      @equity_return = equity_return
      @bond_return = bond_return
      @equity_volatility = equity_volatility
      @bond_volatility = bond_volatility
      @equity_allocation = equity_allocation
      @bond_allocation = 1 - equity_allocation
      @inflation_rate = inflation_rate
      @n_simulations = n_simulations
    end

    def simulate(years: 20)
      endowment_values = Array.new(@n_simulations) { Array.new(years + 1, @initial_value) }

      (0...@n_simulations).each do |i|
        (0...years).each do |year|
          # Simulate returns
          equity_ret = RandomGenerator.normal(mean: @equity_return, std: @equity_volatility)
          bond_ret = RandomGenerator.normal(mean: @bond_return, std: @bond_volatility)

          # Portfolio return
          portfolio_return = @equity_allocation * equity_ret + @bond_allocation * bond_ret

          # Apply return
          endowment_values[i][year + 1] = endowment_values[i][year] * (1 + portfolio_return)

          # Apply inflation-adjusted payout
          inflation_adjusted_payout = @annual_payout * ((1 + @inflation_rate) ** year)
          endowment_values[i][year + 1] -= inflation_adjusted_payout

          # Ensure non-negative
          endowment_values[i][year + 1] = [0, endowment_values[i][year + 1]].max
        end
      end

      endowment_values
    end

    def run(years: 20)
      values = simulate(years: years)
      final_values = values.map { |v| v.last }
      survival_threshold = @initial_value * 0.8
      survival_probability = final_values.count { |v| v >= survival_threshold } / final_values.size.to_f

      {
        endowment_values: values,
        final_values: final_values,
        mean_final: final_values.sum / final_values.size.to_f,
        median_final: final_values.sort[final_values.size / 2],
        std_final: Math.sqrt(final_values.map { |x| (x - mean_final) ** 2 }.sum / final_values.size.to_f),
        survival_probability: survival_probability,
        purchasing_power_threshold: survival_threshold
      }
    end
  end

  # Bayesian Monte Carlo simulation
  class BayesianEndowment
    attr_reader :initial_value, :annual_payout, :prior_equity_return,
                :prior_bond_return, :prior_equity_volatility, :prior_bond_volatility,
                :n_simulations

    def initialize(initial_value:, annual_payout:, prior_equity_return:, 
                   prior_bond_return:, prior_equity_volatility:, prior_bond_volatility,
                   n_simulations: 10000)
      @initial_value = initial_value
      @annual_payout = annual_payout
      @prior_equity_return = prior_equity_return
      @prior_bond_return = prior_bond_return
      @prior_equity_volatility = prior_equity_volatility
      @prior_bond_volatility = prior_bond_volatility
      @n_simulations = n_simulations
    end

    def sample_from_priors
      equity_return = Array.new(@n_simulations) do
        RandomGenerator.normal(mean: @prior_equity_return[:mean], std: @prior_equity_return[:std])
      end
      bond_return = Array.new(@n_simulations) do
        RandomGenerator.normal(mean: @prior_bond_return[:mean], std: @prior_bond_return[:std])
      end
      equity_vol = Array.new(@n_simulations) do
        RandomGenerator.gamma(shape: 2, scale: @prior_equity_volatility)
      end
      bond_vol = Array.new(@n_simulations) do
        RandomGenerator.gamma(shape: 2, scale: @prior_bond_volatility)
      end

      [equity_return, bond_return, equity_vol, bond_vol]
    end

    def simulate(years: 20)
      equity_return, bond_return, equity_vol, bond_vol = sample_from_priors
      endowment_values = Array.new(@n_simulations) { Array.new(years + 1, @initial_value) }

      (0...@n_simulations).each do |i|
        (0...years).each do |year|
          portfolio_return = 0.7 * RandomGenerator.normal(mean: equity_return[i], std: equity_vol[i]) +
                            0.3 * RandomGenerator.normal(mean: bond_return[i], std: bond_vol[i])
          endowment_values[i][year + 1] = endowment_values[i][year] * (1 + portfolio_return) - @annual_payout
          endowment_values[i][year + 1] = [0, endowment_values[i][year + 1]].max
        end
      end

      endowment_values
    end

    def run(years: 20)
      values = simulate(years: years)
      final_values = values.map { |v| v.last }
      sorted_values = final_values.sort

      {
        endowment_values: values,
        final_values: final_values,
        posterior_mean: final_values.sum / final_values.size.to_f,
        posterior_std: Math.sqrt(final_values.map { |x| (x - posterior_mean) ** 2 }.sum / final_values.size.to_f),
        credible_interval_95: [sorted_values[(sorted_values.size * 0.025).to_i], 
                               sorted_values[(sorted_values.size * 0.975).to_i]],
        credible_interval_50: [sorted_values[(sorted_values.size * 0.25).to_i], 
                               sorted_values[(sorted_values.size * 0.75).to_i]]
      }
    end
  end

  # Latin Hypercube Sampling
  class LatinHypercubeSampling
    attr_reader :initial_value, :returns, :volatility, :n_simulations

    def initialize(initial_value:, returns:, volatility:, n_simulations: 10000)
      @initial_value = initial_value
      @returns = returns
      @volatility = volatility
      @n_simulations = n_simulations
    end

    def generate_lhs_samples(n_samples, n_dimensions)
      samples = Array.new(n_samples) { Array.new(n_dimensions) }

      (0...n_dimensions).each do |d|
        perm = (0...n_samples).to_a.shuffle
        (0...n_samples).each do |i|
          samples[i][d] = (perm[i] - 0.5) / n_samples.to_f
        end
      end

      samples
    end

    def simulate_lhs_portfolio(time_horizon: 252)
      lhs_samples = generate_lhs_samples(@n_simulations, 2)

      sampled_returns = lhs_samples.map { |s| @returns + (s[0] - 0.5) * @returns * 0.5 }
      sampled_volatility = lhs_samples.map { |s| @volatility + (s[1] - 0.5) * @volatility * 0.5 }

      dt = 1.0 / time_horizon
      portfolio_values = Array.new(@n_simulations) { Array.new(time_horizon + 1, @initial_value) }

      (0...time_horizon).each do |t|
        (0...@n_simulations).each do |i|
          z = RandomGenerator.normal
          portfolio_return = (sampled_returns[i] - 0.5 * sampled_volatility[i]**2) * dt +
                            sampled_volatility[i] * Math.sqrt(dt) * z
          portfolio_values[i][t + 1] = portfolio_values[i][t] * (1 + portfolio_return)
        end
      end

      portfolio_values
    end

    def run(time_horizon: 252)
      values = simulate_lhs_portfolio(time_horizon: time_horizon)
      final_values = values.map { |v| v.last }
      sorted_values = final_values.sort

      {
        final_values: final_values,
        mean: final_values.sum / final_values.size.to_f,
        std: Math.sqrt(final_values.map { |x| (x - mean) ** 2 }.sum / final_values.size.to_f),
        percentile_5: sorted_values[(sorted_values.size * 0.05).to_i],
        percentile_95: sorted_values[(sorted_values.size * 0.95).to_i],
        all_paths: values
      }
    end
  end
end

# Example usage
puts "Monte Carlo Simulations Portfolio - Ruby Implementation"
puts "=" * 60

# Example 1: Endowment Sustainability
puts "\n1. Endowment Sustainability Simulation"
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
puts "   Mean Final Value: $#{results[:mean_final].round(2)}"
puts "   Survival Probability: #{(results[:survival_probability] * 100).round(2)}%"

# Example 2: Bayesian Monte Carlo
puts "\n2. Bayesian Monte Carlo Simulation"
bayesian_mc = MonteCarlo::BayesianEndowment.new(
  initial_value: 10_000_000.0,
  annual_payout: 315_000.0,
  prior_equity_return: { mean: 0.08, std: 0.02 },
  prior_bond_return: { mean: 0.04, std: 0.01 },
  prior_equity_volatility: 0.16,
  prior_bond_volatility: 0.08,
  n_simulations: 5000
)

bayesian_results = bayesian_mc.run(years: 20)
puts "   Posterior Mean: $#{bayesian_results[:posterior_mean].round(2)}"
puts "   95% Credible Interval: $#{bayesian_results[:credible_interval_95][0].round(2)} - $#{bayesian_results[:credible_interval_95][1].round(2)}"

# Example 3: Latin Hypercube Sampling
puts "\n3. Latin Hypercube Sampling"
lhs_mc = MonteCarlo::LatinHypercubeSampling.new(
  initial_value: 1_000_000.0,
  returns: 0.10,
  volatility: 0.20,
  n_simulations: 5000
)

lhs_results = lhs_mc.run(time_horizon: 252)
puts "   Mean Final Value: $#{lhs_results[:mean].round(2)}"
puts "   5th-95th Percentile: $#{lhs_results[:percentile_5].round(2)} - $#{lhs_results[:percentile_95].round(2)}"

puts "\nAll simulations completed successfully!"
puts "\nNote: For visualization, consider using Ruby libraries like 'gruff' or 'rubyplot' or export data to Python/matplotlib"
