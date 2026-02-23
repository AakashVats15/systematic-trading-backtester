import os

base_path = r"E:\Personal\GitHub\Python Code Repo\systematic-trading-backtester"

# List of folders to create
folders = [
    "backtester",
    "backtester/core",
    "backtester/strategies",
    "backtester/metrics",
    "backtester/reporting",
    "backtester/utils",
    "backtester/data",
    "examples",
    "tests"
]

# List of files to create (relative to base_path)
files = [
    "README.md",
    "pyproject.toml",
    "setup.cfg",
    ".gitignore",

    "backtester/__init__.py",
    "backtester/core/__init__.py",
    "backtester/core/event.py",
    "backtester/core/engine.py",
    "backtester/core/data_handler.py",
    "backtester/core/execution.py",
    "backtester/core/portfolio.py",
    "backtester/core/order.py",
    "backtester/core/fills.py",
    "backtester/core/clock.py",

    "backtester/strategies/__init__.py",
    "backtester/strategies/base_strategy.py",
    "backtester/strategies/momentum.py",
    "backtester/strategies/mean_reversion.py",

    "backtester/metrics/__init__.py",
    "backtester/metrics/performance.py",
    "backtester/metrics/drawdown.py",
    "backtester/metrics/turnover.py",

    "backtester/reporting/__init__.py",
    "backtester/reporting/plots.py",
    "backtester/reporting/report.py",

    "backtester/utils/__init__.py",
    "backtester/utils/logger.py",
    "backtester/utils/config.py",
    "backtester/utils/math_utils.py",

    "backtester/data/__init__.py",
    "backtester/data/loaders.py",
    "backtester/data/synthetic.py",

    "examples/__init__.py",
    "examples/run_momentum.py",
    "examples/run_mean_reversion.py",

    "tests/__init__.py",
    "tests/test_engine.py",
    "tests/test_portfolio.py",
    "tests/test_execution.py",
    "tests/test_strategies.py",
    "tests/test_metrics.py",
    "tests/test_reporting.py",
]

# Create folders
for folder in folders:
    path = os.path.join(base_path, folder)
    os.makedirs(path, exist_ok=True)

# Create files
for file in files:
    file_path = os.path.join(base_path, file)
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Create empty file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass

print("Folder structure created successfully.")
