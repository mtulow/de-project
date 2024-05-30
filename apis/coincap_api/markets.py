import json
import pandas as pd
import datetime as dt
try:
    from dlt.sources.helpers import requests
except ImportError:
    import requests


def get_markets():
    url = "https://api.coincap.io/v2/markets"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    return json.loads(response.content)
    # for line in response.iter_lines():
    #     yield json.loads(line)

def get_market(market_id: str):
    url = f"https://api.coincap.io/v2/markets/{market_id}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def main():
    response_data = get_markets()
    timestamp = response_data['timestamp']
    markets = pd.DataFrame(response_data['data'])
    print('Coincap API 2.0 - `/markets` endpoint:\n')
    print('Response data:', timestamp, dt.datetime.fromtimestamp(timestamp/1000))
    print(markets)
    print()


if __name__ == '__main__':
    print()
    main()
    print()