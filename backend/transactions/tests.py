from contextlib import nullcontext
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from transactions.services import execute_trade
from portfolio.models import Portfolio, Position
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
        self.price = 20

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
        trade = Trade.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            trade_type="buy",
            quantity=self.quantity,
            price=self.price,
        )

        expected_position = Position.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            quantity=self.quantity,
            average_price=self.price,
        )

        position = execute_trade(trade)

        self.assertEqual(position, expected_position)

    def testPositionUpdateBuy(self):
        position = Position.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            quantity=self.quantity,
            average_price=self.price,
        )

        trade = Trade.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            trade_type="buy",
            quantity=self.quantity,
            price=self.price / 2,
        )

        execute_trade(trade)

        expected_average_price = (
            (position.quantity * position.average_price)
            + (trade.quantity * trade.price)
        ) / (position.quantity + trade.quantity)

        expected_position = Position.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            quantity=self.quantity * 2,
            average_price=expected_average_price,
        )  # TODO: WHY IS POSITION 10 OR SOMETHING SOMETHINGS WRONG WITH THE POSITION COUNT

        actual_position = Position.objects.filter(stock_symbol=self.stock_symbol)[0]

        self.assertEqual(expected_position.portfolio, actual_position.portfolio)
        self.assertEqual(expected_position.stock_symbol, actual_position.stock_symbol)
        self.assertEqual(expected_position.quantity, actual_position.quantity)
        self.assertEqual(expected_position.average_price, actual_position.average_price)

    def testPositionUpdateBuy(self):
        position = Position.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            quantity=self.quantity,
            average_price=self.price,
        )

        trade = Trade.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            trade_type="sell",
            quantity=3,
            price=self.price / 2,
        )

        execute_trade(trade)

        expected_position = Position.objects.create(
            portfolio=self.portfolio,
            stock_symbol=self.stock_symbol,
            quantity=position.quantity - trade.quantity,
            average_price=self.price,
        )  # TODO: WHY IS POSITION 10 OR SOMETHING SOMETHINGS WRONG WITH THE POSITION COUNT

        actual_position = Position.objects.filter(stock_symbol=self.stock_symbol)[0]

        self.assertEqual(expected_position.portfolio, actual_position.portfolio)
        self.assertEqual(expected_position.stock_symbol, actual_position.stock_symbol)
        self.assertEqual(expected_position.quantity, actual_position.quantity)
        self.assertEqual(expected_position.average_price, actual_position.average_price)
