import backtrader as bt
from strategies.ml_strategy import MBATS_ML_Strategy
from analyzers.custom_analyzers import MBATS_Risk_Analyzer
from brokers.broker_factory import get_broker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run_engine():
    cerebro = bt.Cerebro()
    print("MBATS Cerebro Engine Initialized.")

    # 1. Add Dummy Data Feed
    dates = [datetime.today() - timedelta(days=x) for x in range(200)]
    df = pd.DataFrame({
        'open': np.random.rand(200) * 10 + 100,
        'high': np.random.rand(200) * 15 + 100,
        'low': np.random.rand(200) * 5 + 100,
        'close': np.random.rand(200) * 10 + 100,
        'volume': np.random.randint(1000, 5000, 200)
    }, index=pd.DatetimeIndex(dates).sort_values())
    
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # 2. Add Strategy
    cerebro.addstrategy(MBATS_ML_Strategy, fast_ma=10, slow_ma=30)

    # 3. Add Analyzers
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(MBATS_Risk_Analyzer, _name='risk_db')

    # 4. Configure Broker via Broker Store
    # Change broker_name to "oanda" or "ib" when you have your API keys ready
    custom_broker = get_broker(broker_name="inbuilt", cash=100000.0, commission=0.001)
    cerebro.broker = custom_broker

    print("\nRunning Backtest...")
    results = cerebro.run()
    strat = results[0]
    
    print("\n--- INBUILT METRICS ---")
    print(f"Max Drawdown: {strat.analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
    print("\nBacktest Complete.")

if __name__ == '__main__':
    run_engine()
