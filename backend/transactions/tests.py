from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
import yfinance as yf

from transactions.services import tradeToPosition
from portfolio.models import Portfolio
from transactions.models import Trade


# Create your tests here.
class TestTransactions(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", password="pass"
        )
        self.portfolio = Portfolio.objects.create(user=self.user)

        self.stock_symbol = "AAPL"
        self.quantity = 5
        self.price = Decimal(yf.Ticker(self.stock_symbol).info["regularMarketPrice"])

    def testCreation(self):
        """
        Test the creation of a trade object
        """
        trade = Trade.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            trade_type="buy",
            quantity=self.quantity,
            price=self.price,
        )

        self.assertEqual(trade.portfolio, self.portfolio)
        self.assertEqual(trade.stock_symbol, self.stock_symbol)
        self.assertEqual(trade.trade_type, "buy")
        self.assertEqual(trade.quantity, self.quantity)
        self.assertEqual(trade.price, self.price)

    def testPositionCreation(self):
        pass

    def testPositionUpdate(self):
        pass
