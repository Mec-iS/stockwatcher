# coding=utf-8

__author__ = 'Lorenzo'

from src.stock import Stock


class Rule:
    """
    A rule is a state that triggers an event when a condition is met.
    A certain level of price or a given date/time can trigger a
    notification or something similar.
    Condition can be a lambda or a standard function that check over price
    or other Stock's attributes.
    """
    def __init__(self, stock, condition):
        # a reference to a Stock
        self.stock = stock if isinstance(stock, Stock) else TypeError(
            'stock should be a Stock()'
        )
        # a reference to a callable
        self.condition = condition if callable(condition) else TypeError(
            'condition should be a callable'
        )

    @property
    def check_condition(self):
        return self.condition(self.stock) if self.stock.price else False

