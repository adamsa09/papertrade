from typing import ParamSpecArgs
import yfinance as yf
from transactions.models import Trade
from portfolio.models import Portfolio, Position


def execute_trade(trade: Trade):
    """
    Create or update a position from a trade
    Function does not save the updated position in the DB.

    Args:
        trade (Trade): the trade to be executed

    Returns:
        position (Position): the position derived from the trade
    """
    if Position.objects.filter(stock_symbol=trade.stock_symbol):
        position = Position.objects.filter(stock_symbol=trade.stock_symbol)[0]

        position = update_position(position, trade)

    else:
        position = new_position(trade)

    return position


def update_position(position: Position, trade: Trade):
    """
    Update a position based on a trade

    Args:
        position (Position): the position to update
        trade (Trade): the trade to use to update the position

    Returns:
        position (Position): the updated position
    """

    updated_average_price = update_average_price(position, trade)
    position.average_price = updated_average_price

    if trade.trade_type == "buy":
        position.quantity = position.quantity + trade.quantity
    elif trade.trade_type == "sell" and trade.quantity <= position.quantity:
        position.quantity = position.quantity - trade.quantity

    
    return position


def new_position(trade: Trade):
    """
    Create a position based on a trade

    Args:
        trade (Trade): the trade to use to update the position

    Returns:
        position (Position): the new position
    """
    if trade.type == "sell":
        return 1

    position = Position(
        portfolio=trade.portfolio,
        stock_symbol=trade.stock_symbol,
        quantity=trade.quantity,
        average_price=trade.price,
    )

    return position


def update_average_price(position: Position, trade: Trade):
    """
    Update the average price of a position

    Args:
        position: the position of which to update the average price
        trade: the trade causing the average price to change
    """
    average_price = (
        (position.quantity * position.average_price) + (trade.quantity * trade.price)
    ) / (position.quantity + trade.quantity)

    return average_price
