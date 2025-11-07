from collections import defaultdict
from django.db import models
import yfinance as yf


# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    cash_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=10000.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_value(self):
        total = self.cash_balance
        for position in self.positions.all():
            total = total + position.market_value()

        return total


class Position(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, related_name="positions", on_delete=models.CASCADE
    )
    stock_symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def market_value(self):
        ticker = yf.Ticker(self.stock_symbol)
        current_price = ticker.info["regularMarketPrice"]
        return current_price * self.quantity
