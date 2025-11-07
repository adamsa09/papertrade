from django.test import TestCase
from .models import Portfolio, Position
from django.contrib.auth import get_user_model
import yfinance as yf

# Create your tests heire.
class TestPortfolio(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user', password='pass')
        self.expected_cash_balance = 10000.00

    def testCreation(self):
        portfolio = Portfolio.objects.create(user=self.user)

        self.assertEqual(portfolio.user, self.user)
        self.assertEqual(portfolio.cash_balance, self.expected_cash_balance)

class TestPosition(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user', password='pass')
        self.portfolio = Portfolio.objects.create(user=self.user)

        self.ticker = 'AAPL'
        self.quantity = 5
        self.average_price = 10

    def testCreation(self):
        position = Position.objects.create(portfolio=self.portfolio, stock_symbol=self.ticker, quantity=self.quantity, average_price=self.average_price)
        
        self.assertEqual(position.portfolio, self.portfolio)
        self.assertEqual(position.stock_symbol, self.ticker)
        self.assertEqual(position.quantity, self.quantity)
        self.assertEqual(position.average_price, self.average_price)

    def testMarketValue(self):
        position = Position.objects.create(portfolio=self.portfolio, stock_symbol=self.ticker, quantity=self.quantity, average_price=self.average_price)

        expected_market_value = yf.Ticker(self.ticker).info['regularMarketPrice'] * self.quantity 

        self.assertEqual(position.market_value(), expected_market_value)

    def testFk(self): 
        position = Position.objects.create(portfolio=self.portfolio, stock_symbol=self.ticker, quantity=self.quantity, average_price=self.average_price)
        
        self.assertEqual(position.portfolio, self.portfolio)
        





        
