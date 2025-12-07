import subprocess
import json
import requests

def get_btc_price_brl():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "brl"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["bitcoin"]["brl"]


endereco = "bc1q0v53ch4qgcg36mkjmp674wspxzphxghvf74a62"

url = f"https://blockstream.info/api/address/{endereco}"

# Executa o curl
resultado = subprocess.check_output(
    ["curl", "-s", url]
).decode()

# Converte JSON
dados = json.loads(resultado)

funded = dados["chain_stats"]["funded_txo_sum"]
spent = dados["chain_stats"]["spent_txo_sum"]

saldo_sats = funded - spent
saldo_btc = saldo_sats / 100_000_000

print(f"{saldo_btc:.8f}", "BTC")
