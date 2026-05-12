#!/bin/bash
# Linux Setup Script for Monte Carlo Simulations
# This script installs dependencies and sets up the environment for Linux

set -e  # Exit on any error

echo "=== Monte Carlo Simulations - Linux Setup ==="
echo "This script will install dependencies and configure the environment for Linux."
echo

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: This script is designed for Linux systems."
    echo "Current OS: $OSTYPE"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python installation
echo "=== Checking Python Installation ==="
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python3 found: $PYTHON_VERSION"
else
    echo "❌ Python3 not found. Please install Python 3.7+ first."
    echo "On Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "On CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "On Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

# Check pip installation
echo "=== Checking pip Installation ==="
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
else
    echo "❌ pip3 not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    else
        echo "Please install pip3 manually."
        exit 1
    fi
fi

# Install Python dependencies
echo "=== Installing Python Dependencies ==="
echo "This may take a few minutes..."

# Upgrade pip
python3 -m pip install --upgrade pip

# Install required packages
python3 -m pip install numpy>=1.19.0
python3 -m pip install pandas>=1.3.0
python3 -m pip install matplotlib>=3.3.0
python3 -m pip install seaborn>=0.11.0
python3 -m pip install scipy>=1.7.0

# Install optional packages for enhanced functionality
echo "=== Installing Optional Dependencies ==="
python3 -m pip install jupyter  # For notebook support
python3 -m pip install openpyxl  # For Excel export
python3 -m pip install plotly  # For interactive plots

# Set up matplotlib for headless environments
echo "=== Configuring Matplotlib ==="
export MPLBACKEND=Agg
echo 'export MPLBACKEND=Agg' >> ~/.bashrc

# Create output directory
echo "=== Creating Directories ==="
mkdir -p output
mkdir -p logs
mkdir -p data

# Test installation
echo "=== Testing Installation ==="
python3 -c "
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
print('✅ All dependencies imported successfully')
print(f'NumPy version: {np.__version__}')
print(f'Pandas version: {pd.__version__}')
print(f'Matplotlib version: {matplotlib.__version__}')
print(f'Seaborn version: {sns.__version__}')
print(f'SciPy version: {stats.__version__}')
"

if [ $? -eq 0 ]; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Create launcher script
echo "=== Creating Launcher Script ==="
cat > run_monte_carlo.sh << 'EOF'
#!/bin/bash
# Monte Carlo Simulations Launcher for Linux

# Set environment variables
export MPLBACKEND=Agg
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Create timestamp for logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/monte_carlo_${TIMESTAMP}.log"

echo "Starting Monte Carlo Simulations..."
echo "Log file: $LOG_FILE"

# Run main simulation
python3 monte_carlo_simulations.py 2>&1 | tee -a "$LOG_FILE"

# Run case studies if requested
if [ "$1" = "--case-studies" ]; then
    echo "Running case studies..."
    python3 case_studies.py 2>&1 | tee -a "$LOG_FILE"
fi

echo "Simulation completed. Check $LOG_FILE for details."
EOF

chmod +x run_monte_carlo.sh

# Create test script
echo "=== Creating Test Script ==="
cat > test_linux_compatibility.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for Linux compatibility
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test all required imports"""
    try:
        import numpy as np
        import pandas as pd
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic Monte Carlo functionality"""
    try:
        # Simple test simulation
        np.random.seed(42)
        returns = np.random.normal(0.08, 0.16, 1000)
        final_values = 1000000 * (1 + returns)
        
        mean_value = np.mean(final_values)
        percentile_5 = np.percentile(final_values, 5)
        percentile_95 = np.percentile(final_values, 95)
        
        print(f"✅ Basic functionality test passed")
        print(f"   Mean final value: ${mean_value:,.2f}")
        print(f"   5th percentile: ${percentile_5:,.2f}")
        print(f"   95th percentile: ${percentile_95:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_file_operations():
    """Test file read/write operations"""
    try:
        # Test writing CSV
        import pandas as pd
        test_data = pd.DataFrame({
            'simulation_id': range(10),
            'final_value': np.random.uniform(800000, 1200000, 10)
        })
        test_data.to_csv('output/test_output.csv', index=False)
        
        # Test reading back
        read_data = pd.read_csv('output/test_output.csv')
        
        # Clean up
        os.remove('output/test_output.csv')
        
        print("✅ File operations test passed")
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def main():
    print("=== Linux Compatibility Test ===")
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Monte Carlo simulations.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

chmod +x test_linux_compatibility.py

echo ""
echo "=== Setup Complete ==="
echo "✅ Dependencies installed"
echo "✅ Environment configured"
echo "✅ Launcher script created: run_monte_carlo.sh"
echo "✅ Test script created: test_linux_compatibility.py"
echo ""
echo "Next steps:"
echo "1. Run the test: python3 test_linux_compatibility.py"
echo "2. Run simulations: ./run_monte_carlo.sh"
echo "3. Run with case studies: ./run_monte_carlo.sh --case-studies"
echo ""
echo "For help or issues, check the logs directory or run:"
echo "python3 linux_compatibility_check.py"
