

# def get_exchanges():
#     url = "https://api.coincap.io/v2/exchanges"

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     for data in response.iter_lines():
#         yield json.loads(data)


# def get_exchange(exchange_id: str):
#     url = f"https://api.coincap.io/v2/exchanges/{exchange_id}"

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)
#     return response.json()
    
# def main():
    
#     exchanges = get_exchanges()
#     for exchange in exchanges:
#         print()
#         print(exchange)

# if __name__ == '__main__':
#     print()
#     main()
#     print()