try:
    from dlt.sources.helpers import requests
except ImportError:
    import requests

import datetime as dt


def get_candles(quote_id: str,
                interval: str = 'h12',
                base_id: str = 'bitcoin',
                exchange: str = 'poloniex',
                start: str | dt.datetime | None = None,
                end: str | dt.datetime | None = None,
                data: dict = None,
                headers: dict = None,
    ):
    """Get candles for a specific asset on a specific exchange.

    Args:
        quote_id (str): The quote asset id.
        interval (str): The candle interval. Options are: [`m1`, `m5`, `m15`, `m30`, `h1`, `h2`, `h4`, `h8`, `h12`, `d1`, `w1`]
        base_id (str): The base asset id. Defaults to `bitcoin`.
        exchange (str): The exchange id. Defaults to `poloniex`.
        start (str | dt.datetime | None): The start time for the candles.
        end (str | dt.datetime | None): The end time for the candles.
    """
    url = 'https://api.coincap.io/v2/candles'

    headers = {}
    data = data or dict(quoteId=quote_id,
                        interval=interval,
                        baseId=base_id,
                        exchange=exchange,)
    if start:
        data['start'] = start
    if end:
        data['end'] = end

    response = requests.request("GET", url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def main():
    token = 'bitcoin'
    base_asset = 'ethereum'
    interval = 'h12'
    exchange = 'poloniex'

    response_data = get_candles(token,
                                interval=interval,
                                base_id=base_asset,
                                exchange=exchange)
    
    candles = response_data['data']
    timestamp = response_data['timestamp']
    
    print(f'{timestamp = }\n{candles = }')

if __name__ == '__main__':
    print()
    main()
    print()