import requests
import time

def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ethereum", "vs_currencies": "usd"}
    return requests.get(url, params=params).json()["ethereum"]["usd"]

while True:
    try:
        price = get_eth_price()
        print(f"Preço do Ethereum: ${price:.2f} USD")
    except Exception as e:
        print("Erro ao obter o preço:", e)
    time.sleep(20)
