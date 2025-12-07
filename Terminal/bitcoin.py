import requests

def get_bitcoin_price():
    try:
        # API do CoinGecko (simples e gratuita)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "brl"
        }
        
        # Timeout de 2s para não travar o terminal se a net estiver ruim
        resp = requests.get(url, params=params, timeout=2)
        resp.raise_for_status()
        
        preco = resp.json()["bitcoin"]["brl"]
        
        # Formatação manual para garantir padrão BR (1.000,00) sem depender de locale do sistema
        preco_formatado = f"{preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        return f"R$ {preco_formatado}"
        
    except Exception:
        # Retorno discreto em caso de erro (sem traceback gigante)
        return "R$ ----"

if __name__ == "__main__":
    print(get_bitcoin_price())
