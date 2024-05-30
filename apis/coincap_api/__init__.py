try:
    from dlt.sources.helpers import requests
except ImportError:
    import requests

import dlt
import json
import duckdb
import pandas as pd
import datetime as dt

# from apis.coincap_api.assets import (get_asset, get_assets,
#                                      get_asset_market)
# from apis.coincap_api.exchanges import get_exchanges
# from apis.coincap_api.markets import get_markets
from apis.coincap_api.candles import get_candles




def send_get_request(url: str, headers: dict = {}, data: dict = {}):
    response = requests.request("GET", url, headers=headers, data=data)
    response.raise_for_status()
    return response

# Create demo pipeline to duckdb
def demo_candles_endpoint(token: str = 'ethereum'):
    # Create dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name='coincap_api',
        destination='duckdb',
        dataset_name='candles_endpoint',
    )

    # Get candles data
    candles_data = get_candles('ethereum')

    # Ingest data into pipeline
    table_name = f'{token}_candles'
    pipeline.run(candles_data,
                 table_name=table_name,
                 write_disposition='overwrite')
    




    exchanges = get_exchanges('binance')
    for exchange in exchanges:
        print()
        print(exchange)


def demo_markets_endpoint():
    # 
    pipeline = dlt.pipeline(
        pipeline_name='markets',
        destination='duckdb',
        dataset_name='markets',
    )

    response_data = get_markets()
    timestamp = response_data['timestamp']
    markets = pd.DataFrame(response_data['data'])
    print('Coincap API 2.0 - `/markets` endpoint:\n')
    print('Response data:', timestamp, dt.datetime.fromtimestamp(timestamp/1000))
    print(markets)
    print()