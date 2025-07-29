from django.db import models

# Create your models here.
class CryptoPrice(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    percent_change = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    circulating_supply = models.BigIntegerField(null=True, blank=True)
    volume_24h = models.BigIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.symbol}: {self.price}"
