# Systematic Trading Backtester

A modular, event‑driven backtesting engine for systematic trading in Python.  
The framework supports vectorised strategy logic, slippage‑aware execution, portfolio accounting, and full performance reporting with metrics and plots.

---

## 🚀 Features

- Event‑driven architecture (MarketEvent, SignalEvent, OrderEvent, FillEvent)
- Vectorised NumPy‑based strategy computations
- Modular strategy API (momentum, mean‑reversion, custom strategies)
- Execution model with market orders, slippage, and fill simulation
- Portfolio accounting (positions, PnL, equity curve)
- Performance metrics (Sharpe, drawdowns, turnover, returns)
- Reporting utilities with plots and summary tables
- Clean, extensible Python‑only codebase

---

## 📁 Project Structure

```
systematic-trading-backtester/
│
├── backtester/
│   ├── core/              # Event loop, data handler, execution, portfolio
│   ├── strategies/        # Strategy modules (momentum, mean reversion, etc.)
│   ├── metrics/           # Sharpe, drawdown, turnover, performance stats
│   ├── reporting/         # Plotting + backtest report generation
│   ├── utils/             # Logging, config, math helpers
│   └── data/              # Data loaders + synthetic data generators
│
├── examples/              # Example scripts to run strategies
├── tests/                 # Unit tests for engine, strategies, metrics
│
├── README.md
├── pyproject.toml         # Packaging + dependencies
├── setup.cfg              # Linting + formatting config
└── .gitignore
```

### Folder Overview

| Folder | Purpose |
|--------|---------|
| **backtester/core** | Implements the event‑driven engine, order handling, fills, portfolio logic, and data ingestion. |
| **backtester/strategies** | Contains strategy classes. Each strategy inherits from `BaseStrategy`. |
| **backtester/metrics** | Computes performance statistics such as Sharpe ratio, drawdowns, and turnover. |
| **backtester/reporting** | Generates plots and summary reports after a backtest. |
| **backtester/utils** | Logging, configuration helpers, and mathematical utilities. |
| **backtester/data** | Data loaders and synthetic data generation tools. |
| **examples** | Ready‑to‑run scripts demonstrating how to execute a backtest. |
| **tests** | Unit tests ensuring correctness and stability. |

---

## 🧠 How to Use This Backtester

### 1. Install Dependencies

From the project root:

```bash
pip install -e .
```

This installs the package in editable mode.

---

### 2. Run an Example Strategy

Example: run the momentum strategy.

```bash
python examples/run_momentum.py
```

Example: run the mean‑reversion strategy.

```bash
python examples/run_mean_reversion.py
```

Each script:

- Loads data (CSV or synthetic)
- Instantiates the strategy
- Runs the event‑driven engine
- Produces performance metrics + plots

---

## 🛠 Creating Your Own Strategy

1. Create a new file in:

```
backtester/strategies/my_strategy.py
```

2. Inherit from `BaseStrategy`:

```python
from backtester.strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def generate_signals(self, data):
        # vectorised NumPy logic here
        return signals
```

3. Add a script in `examples/` to run it.

---

## 📊 Output

After running a backtest, the engine produces:

- Equity curve plot
- Drawdown plot
- Performance summary (Sharpe, returns, volatility)
- Turnover and trade statistics
- CSV/JSON logs (optional)

---

## 🤝 Contributing

Pull requests are welcome.  
Please ensure new features include tests and documentation.