import backtrader as bt

def get_broker(broker_name="inbuilt", **kwargs):
    """
    MBATS Broker Store: Initializes and returns the requested broker.
    Supports 'inbuilt' (backtesting), 'oanda', and 'ib' (Interactive Brokers).
    """
    if broker_name == "oanda":
        print("[Broker Store] Initializing Oanda V20 API...")
        # Note: Backtrader's Oanda store requires actual API keys to initialize successfully
        try:
            store = bt.stores.OandaV20Store(
                token=kwargs.get('token', 'DUMMY_TOKEN'),
                account=kwargs.get('account', 'DUMMY_ACCOUNT'),
                practice=True # Forces paper trading
            )
            return store.getbroker()
        except Exception as e:
            print(f"[Broker Store Error] Oanda initialization failed: {e}")
            print("Falling back to inbuilt broker...")
            return get_broker("inbuilt", **kwargs)

    elif broker_name == "ib":
        print("[Broker Store] Initializing Interactive Brokers API...")
        # Requires Trader Workstation (TWS) or IB Gateway running locally
        try:
            store = bt.stores.IBStore(
                host=kwargs.get('host', '127.0.0.1'),
                port=kwargs.get('port', 7497), # 7497 is standard for paper trading
                clientId=kwargs.get('client_id', 1)
            )
            return store.getbroker()
        except Exception as e:
            print(f"[Broker Store Error] IB initialization failed: {e}")
            print("Falling back to inbuilt broker...")
            return get_broker("inbuilt", **kwargs)

    else:
        print("[Broker Store] Initializing Inbuilt Backtesting Broker...")
        broker = bt.brokers.BackBroker()
        broker.setcash(kwargs.get('cash', 100000.0))
        broker.setcommission(commission=kwargs.get('commission', 0.001))
        return broker
