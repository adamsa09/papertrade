from django.db import models
from portfolio.models import Portfolio, Position

# Create your models here.
class Trade(models.Model):
    TRADE_TYPE_CHOICES = (
            ('buy', 'buy'),

            ('sell', 'sell')
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    trade_type = models.CharField(choices=TRADE_TYPE_CHOICES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    executed_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return self.price * self.quantity
