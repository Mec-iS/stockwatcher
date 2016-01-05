# coding=utf-8
import unittest
from datetime import datetime

__author__ = 'Lorenzo'

from src.stock import Stock


class StockDMAC(unittest.TestCase):
    """Test time series and DMAC analysis"""
    @classmethod
    def setUpClass(cls):
        cls.stock = Stock("GOOG")
        # create a price history
        cls.trend_fixture(
            [82, 79, 84.1, 85.6, 80.9, 81.2, 81.5, 81.7, 82.0, 82.2, 82.5]
        )

    def setUp(self):
        pass

    def trend_fixture(self, prices):
        """Create new prices in price history from a list of Float.
    To be used in the tests below."""
        return [self.stock.update(datetime(2015, 12, i+1), price=p)
                for i, p in enumerate(prices)]

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass