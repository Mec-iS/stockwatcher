# coding=utf-8
import unittest
from datetime import date, timedelta

__author__ = 'Lorenzo'

from src.stock import Stock
from src.timeseries import TimeSeries


class StockDMAC(unittest.TestCase):
    """Test time series and DMAC analysis"""
    @classmethod
    def setUpClass(cls):
        cls.stock = Stock("GOOG")

    def trend_fixture(self, prices):
        """Create new prices in price history from a list of Float.
    To be used in the tests below."""
        return [
            self.stock.update(date.today() + timedelta(days=-i), price=p)
            for i, p in enumerate(prices)
        ]

    def setUp(self):
        # create a price history
        self.trend_fixture(
            [82, 79, 84.1, 85.6, 80.9, 81.2, 81.5, 81.7, 82.0, 82.2, 82.5]
        )
        # create a DMAC object for the stock
        self.timeseries = TimeSeries(self.stock)

    def test_should_create_time_series(self):
        # print(self.stock.price_history)
        self.assertTrue(len(self.stock.price_history) > 6)

    def test_should_calculate_stma(self):
        stma = self.timeseries.calculate_stma_ltma(date.today(), period='short')
        #print('STMA', stma)
        self.assertAlmostEqual(stma, 82.16, delta=0.0001)

    def test_should_raise_error_in_calculate(self):
        with self.assertRaises(ValueError):
            self.timeseries.calculate_stma_ltma(date.today(), period='abc')
            self.timeseries.calculate_stma_ltma(date.today(), period=1)

    def test_should_calculate_ltma(self):
        ltma = self.timeseries.calculate_stma_ltma(date.today(), period='long')
        #print('LTMA', ltma)
        self.assertAlmostEqual(ltma, 82.07, delta=0.0001)

    def tearDown(self):
        print(self.stock) if self.stock.price is not None else None
        print(self.timeseries) if self.stock.price is not None else None
        print('\n')
        del self.timeseries

    @classmethod
    def tearDownClass(cls):
        del cls.stock


if __name__ == "__main__":
    unittest.main()