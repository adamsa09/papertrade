from typing import ParamSpecArgs
import yfinance as yf
from transactions.models import Trade 
from portfolio.models import Portfolio, Position

def tradeToPosition(trade):
    """
    Create or update a position from a trade

    Args:
        trade (Trade): the trade to be executed

    Returns:
        position (Position): the position derived from the trade
    """
    pass
