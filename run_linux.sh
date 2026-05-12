#!/bin/bash
# Linux launcher for Monte Carlo Simulations

# Set matplotlib backend for headless environments
export MPLBACKEND=Agg

# Run the main simulation
python3 monte_carlo_simulations.py

# Run case studies
python3 case_studies.py
