from rest_framework import serializers
from .models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = ['symbol', 'price', 'percent_change', 'last_updated']
        read_only_fields = ['last_updated']

# serializers.py
class CryptoPriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = [
            "name", "symbol", "price", "percent_change",
            "market_cap", "circulating_supply", "volume_24h",
            "last_updated"
        ]
