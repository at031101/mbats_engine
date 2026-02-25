import backtrader as bt
import psycopg2
from datetime import datetime

class PostgresDataFeed(bt.feed.DataBase):
    """
    Custom DataFeed for pulling pricing data from a Postgres Security Master DB.
    Expected Postgres table schema: ticker, datetime, open, high, low, close, volume
    """
    
    # Define customizable parameters for the database connection
    params = (
        ('host', 'localhost'),
        ('database', 'mbats_db'),
        ('user', 'postgres'),
        ('password', 'password'),
        ('port', '5432'),
        ('ticker', 'AAPL'), # Target security
    )

    def start(self):
        """Called right before the backtest starts. We establish the DB connection here."""
        super().start()
        print(f"Connecting to Security Master DB for {self.p.ticker}...")
        
        try:
            self.conn = psycopg2.connect(
                host=self.p.host,
                database=self.p.database,
                user=self.p.user,
                password=self.p.password,
                port=self.p.port
            )
            self.cursor = self.conn.cursor()
            
            # Querying the database. ORDER BY datetime ASC is critical for Backtrader!
            query = f"""
                SELECT datetime, open, high, low, close, volume 
                FROM security_master 
                WHERE ticker = '{self.p.ticker}' 
                ORDER BY datetime ASC;
            """
            self.cursor.execute(query)
            
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise e

    def stop(self):
        """Called when the backtest finishes. Clean up connections."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Database connection closed.")
        super().stop()

    def _load(self):
        """Called by Cerebro to fetch the next tick/bar of data."""
        row = self.cursor.fetchone()
        
        if not row:
            return False  # Return False to tell Cerebro there is no more data

        # Unpack the row (Assuming format: datetime, open, high, low, close, volume)
        dt, o, h, l, c, v = row

        # Populate Backtrader's standard line objects
        self.lines.datetime[0] = bt.date2num(dt)
        self.lines.open[0] = float(o)
        self.lines.high[0] = float(h)
        self.lines.low[0] = float(l)
        self.lines.close[0] = float(c)
        self.lines.volume[0] = float(v)
        self.lines.openinterest[0] = 0.0 # Set to 0 if not tracking open interest

        return True
