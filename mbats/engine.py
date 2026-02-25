import backtrader as bt
from datafeeds.postgres_feed import PostgresDataFeed

def run_engine():
    cerebro = bt.Cerebro()
    print("MBATS Cerebro Engine Initialized.")

    # 1. Add Custom Postgres DataFeed
    # Note: This will fail to connect unless you actually have a local Postgres 
    # database running with these credentials and a 'security_master' table.
    try:
        data = PostgresDataFeed(
            host='localhost',
            database='mbats_db',
            user='postgres',
            password='password',
            ticker='AAPL'
        )
        cerebro.adddata(data)
        print("Postgres DataFeed added to Cerebro.")
    except Exception as e:
        print("Skipping DataFeed addition due to missing DB connection.")

    # Run Cerebro (it won't do much yet without a strategy)
    cerebro.run()

if __name__ == '__main__':
    run_engine()
