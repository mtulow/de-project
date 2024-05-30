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
                payload: dict = {},
                headers: dict = {},
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
    url = "https://api.coincap.io/v2/candles?exchange=poloniex&interval=h8&baseId=ethereum&quoteId=bitcoin"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()


def main():
    token = 'ethereum'
    base_asset = 'bitcoin'
    interval = 'h12'
    exchange = 'poloniex'


    candles = get_candles(token,
                          interval=interval,
                          base_id=base_asset,
                          exchange=exchange)
    for candle in candles:
        print(candle)

if __name__ == '__main__':
    print()
    main()
    print()