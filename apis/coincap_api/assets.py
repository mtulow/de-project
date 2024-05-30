try:
    from dlt.sources.helpers import requests
except ImportError:
    import requests

# from dlt.common.

def send_get_request(url: str, headers: dict = {}, data: dict = {}):
    response = requests.request("GET", url, headers=headers, data=data)
    response.raise_for_status()
    return response

def get_asset(asset_id: str, data: dict = {}, headers: dict = {}):
    def wrapper(get_request):
        url = f"https://api.coincap.io/v2/assets/{asset_id}"
        response = get_request(url, headers=headers, data=data)
        for key in response.json():
            yield key, response.json()[key]
    return wrapper


def get_assets():
    url = "https://api.coincap.io/v2/assets"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = response.json()
    for key in response_data:
        yield key, response_data[key]
        
def get_asset_market(asset_id: str):
    url = f'https://api.coincap.io/v2/assets/{asset_id}/markets'

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    for k,v in data.items():
        yield k, v