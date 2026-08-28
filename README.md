# KrakenBot

KrakenBot is a modular cryptocurrency paper-trading and backtesting system built in Python.

## Overview

KrakenBot analyzes cryptocurrency market conditions, generates trade decisions, applies risk controls, and manages simulated paper trades.

The project is currently configured for **PAPER trading**.

## Current Features

- Market scanning
- EMA and RSI indicators
- Strategy scoring
- Market filtering
- Paper trading
- Take-profit management
- Stop-loss management
- Position persistence
- Restart and position recovery
- Risk management
- Daily trade limits
- Daily loss limits
- Trading-session controls
- Trade journaling
- Trade analytics
- Trade intelligence
- Historical backtesting

## Risk Management

The paper-trading system includes safeguards including:

- Maximum daily trades
- Maximum daily loss
- Trade cooldown periods
- Trading-session restrictions
- Position-state persistence

## Testing

KrakenBot has been manually tested for:

- Position persistence
- Trade lifecycle management
- Take-profit execution
- Stop-loss execution
- Restart and position recovery
- Restart → recovery → take-profit workflow

## Backtesting

The project includes a historical backtesting workflow using:

- `run_backtest.py`
- `backtester.py`
- `backtest_journal.py`
- `test_data.py`

## Project Structure

### Trading Engine

- `main_bot.py`
- `decision.py`
- `strategy.py`
- `strategy_engine.py`
- `market_filter.py`
- `session_manager.py`

### Paper Trading

- `paper_trader.py`
- `risk_manager.py`
- `strategy_context.py`

### Backtesting

- `backtester.py`
- `run_backtest.py`
- `backtest_journal.py`
- `test_data.py`

### Analytics

- `analytics.py`
- `trade_analyzer.py`
- `trade_intelligence.py`
- `report.py`
- `journal_v2.py`

### Automation

- `bot.py`
- `bot_runner.py`
- `scheduler.py`

## Configuration

KrakenBot is currently configured for paper trading.

Sensitive local configuration and trading state are excluded from version control through `.gitignore`.

## Future Development

Planned improvements include:

- Automated test suite with pytest
- Improved backtesting and performance metrics
- CI/CD integration
- Docker containerization
- Cloud deployment experiments
- Monitoring and alerting
- Strategy optimization

## Disclaimer

This project is an educational software-engineering project focused on Python, trading-system architecture, testing, automation, and DevOps practices.

It is not financial advice and is not intended to provide investment recommendations.
