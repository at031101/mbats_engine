import backtrader as bt
import json
import boto3
from datetime import datetime

class MBATS_Risk_Analyzer(bt.Analyzer):
    """
    Combines the Transaction, Performance, and Run Record Analyzers.
    Routes data to the Risk Database and Object Store.
    """
    def __init__(self):
        self.trades = []
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def notify_trade(self, trade):
        """Triggered every time a trade closes."""
        if trade.isclosed:
            self.trades.append({
                'trade_id': trade.ref,
                'pnl': trade.pnl,
                'pnl_with_commission': trade.pnlcomm,
                'bars_in_trade': trade.barlen
            })

    def stop(self):
        """Triggered at the end of the backtest."""
        # 1. Performance Metrics
        total_trades = len(self.trades)
        net_pnl = sum(t['pnl_with_commission'] for t in self.trades) if total_trades > 0 else 0.0
        
        self.rets = {
            'run_id': self.run_id,
            'total_trades': total_trades,
            'net_pnl': round(net_pnl, 2)
        }

        # 2. Push to Risk Database (Mocked Postgres Connection)
        print("\n--- ANALYZER OUTPUT ---")
        print(f"[Risk Database] Pushing Performance Metrics: {self.rets}")
        # In production: engine.execute("INSERT INTO risk_metrics ...")

        # 3. Push to Object Store (Mocked AWS S3 Connection)
        print(f"[Object Store] Pushing {total_trades} transaction records to S3...")
        try:
            # We mock the S3 client here so it doesn't crash without AWS credentials
            # s3 = boto3.client('s3')
            # s3.put_object(Bucket='mbats-transaction-logs', Key=f'run_{self.run_id}.json', Body=json.dumps(self.trades))
            print("[Object Store] Transaction log upload simulated successfully.")
        except Exception as e:
            print(f"[Object Store Error]: {e}")

    def get_analysis(self):
        return self.rets
