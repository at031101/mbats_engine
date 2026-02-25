import backtrader as bt
import mlflow
from indicators.custom_indicators import CustomVolatilityIndicator

class MBATS_ML_Strategy(bt.Strategy):
    """
    Core strategy class integrated with MLFlow.
    """
    params = (
        ('fast_ma', 10),
        ('slow_ma', 30),
        ('mlflow_experiment', 'MBATS_Backtests'),
        ('run_name', 'MA_Crossover_v1')
    )

    def __init__(self):
        # 1. Initialize Inbuilt and Custom Indicators
        self.sma_fast = bt.indicators.SMA(period=self.params.fast_ma)
        self.sma_slow = bt.indicators.SMA(period=self.params.slow_ma)
        self.custom_vol = CustomVolatilityIndicator(period=14)
        
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

        # 2. Initialize MLFlow Logging
        mlflow.set_experiment(self.params.mlflow_experiment)
        self.mlflow_run = mlflow.start_run(run_name=self.params.run_name)
        
        # Log our strategy parameters to MLFlow
        mlflow.log_param("fast_ma", self.params.fast_ma)
        mlflow.log_param("slow_ma", self.params.slow_ma)

    def next(self):
        # Basic trading logic
        if not self.position:
            if self.crossover > 0: # Fast crosses above slow
                self.buy()
        elif self.crossover < 0:   # Fast crosses below slow
            self.close()

    def stop(self):
        # 3. Log results to MLFlow at the end of the run
        final_value = self.broker.getvalue()
        print(f"Ending Portfolio Value: {final_value}")
        
        # Log final equity metric
        mlflow.log_metric("final_portfolio_value", final_value)
        
        # Close the MLFlow run
        mlflow.end_run()
