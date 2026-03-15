import requests
from urllib.parse import unquote


def extrair_info_link(link):

    partes = link.split("/")

    appid = partes[5]
    nome_item = unquote(partes[6])

    return appid, nome_item


def pegar_preco(link, currency=1):

    appid, nome_item = extrair_info_link(link)

    url = "https://steamcommunity.com/market/priceoverview/"

    params = {
        "appid": appid,
        "market_hash_name": nome_item,
        "currency": currency
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.get(url, params=params, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()

        if not data.get("success"):
            return None

    except:
        return None

    return {
        "item": nome_item,
        "lowest_price": data.get("lowest_price"),
        "median_price": data.get("median_price"),
        "volume": data.get("volume")
    }
