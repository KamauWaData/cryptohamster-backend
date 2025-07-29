import requests
from django.core.management.base import BaseCommand
from cryptoprices.models import CryptoPrice

BINANCE_ENDPOINT = "https://api.binance.com/api/v3/ticke/24hr"
TARGET_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
TOKEN_INFO = {
    "BTCUSDT": {"name": "Bitcoin", "supply": 19624123},
    "ETHUSDT": {"name": "Ethereum", "supply": 120180349},
    "BNBUSDT": {"name": "BNB", "supply": 166801148},
    "SOLUSDT": {"name": "Solana", "supply": 448534948},
    "XRPUSDT": {"name": "XRP", "supply": 55866695975},
    "DOGEUSDT": {"name": "Dogecoin", "supply": 144054906384},
    "ADAUSDT": {"name": "Cardano", "supply": 35137784530},
    "AVAXUSDT": {"name": "Avalanche", "supply": 393107865},
    "DOTUSDT": {"name": "Polkadot", "supply": 1372107700},
    "TRXUSDT": {"name": "TRON", "supply": 87699633974},
    "MATICUSDT": {"name": "Polygon", "supply": 9918192050},
    "LINKUSDT": {"name": "Chainlink", "supply": 587099971},
    "TONUSDT": {"name": "Toncoin", "supply": 3474484451},
    "LTCUSDT": {"name": "Litecoin", "supply": 74509431},
    "SHIBUSDT": {"name": "Shiba Inu", "supply": 589289410000000},
    "BCHUSDT": {"name": "Bitcoin Cash", "supply": 19730893},
    "UNIUSDT": {"name": "Uniswap", "supply": 598736259},
    "ETCUSDT": {"name": "Ethereum Classic", "supply": 147264885},
    "ICPUSDT": {"name": "Internet Computer", "supply": 460196628},
    "XLMUSDT": {"name": "Stellar", "supply": 28734614857},
    "APTUSDT": {"name": "Aptos", "supply": 448582036},
    "HBARUSDT": {"name": "Hedera", "supply": 36071008397},
    "FILUSDT": {"name": "Filecoin", "supply": 560080023},
    "ARBUSDT": {"name": "Arbitrum", "supply": 2928250643},
    "NEARUSDT": {"name": "NEAR Protocol", "supply": 1135416181},
    "VETUSDT": {"name": "VeChain", "supply": 72714516834},
    "GRTUSDT": {"name": "The Graph", "supply": 9541887410},
    "INJUSDT": {"name": "Injective", "supply": 93555655},
    "TIAUSDT": {"name": "Celestia", "supply": 177790106},
    "RUNEUSDT": {"name": "THORChain", "supply": 337831100},
}


class Command(BaseCommand):
    help = "Fetches cryptocurrency prices from Binance and updates the database." \
    ""

    def handle(self, *args, **kwargs):
        response = requests.get(BINANCE_ENDPOINT)
        if response.status_code != 200:
            self.stderr.write("Failed to fetch data from Binance API.")
            return
        
        data = response.json()
        for entry in data:
            if entry['symbol'] in TARGET_SYMBOLS:
                price = float(entry['lastPrice'])
                change = float(entry['priceChangePercent'])

                CryptoPrice.objects.update_or_create(
                    symbol=entry['symbol'],
                    defaults={
                        'price': price,
                        'percent_change': change
                    }
                )
            self.stdout.write("Successfully updated cryptocurrencies prices .")

def handle(self, *args, **kwargs):
    response = requests.get(BINANCE_ENDPOINT)
    data = response.json()
    for entry in data:
        symbol = entry["symbol"]
        if symbol in TOKEN_INFO:
            price = float(entry["lastPrice"])
            percent_change = float(entry["priceChangePercent"])
            volume = float(entry["quoteVolume"])
            supply = TOKEN_INFO[symbol]["supply"]
            market_cap = price * supply

            CryptoPrice.objects.update_or_create(
                symbol=symbol,
                defaults={
                    "name": TOKEN_INFO[symbol]["name"],
                    "price": price,
                    "percent_change": percent_change,
                    "volume_24h": volume,
                    "circulating_supply": supply,
                    "market_cap": market_cap,
                }
            )