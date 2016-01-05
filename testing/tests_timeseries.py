# coding=utf-8
import unittest
from datetime import date, timedelta
import random

__author__ = 'Lorenzo'

from src.stock import Stock
from src.timeseries import TimeSeries


class StockDMACscenario(unittest.TestCase):
    """Test time series and DMAC analysis in a complete random scenario"""
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
        test = [round(random.uniform(80.01, 83.01), 2) for _ in range(20)]
        random.shuffle(test)
        self.trend_fixture(test)
        # create a DMAC object for the stock
        self.timeseries = TimeSeries(self.stock)

    def test_should_create_time_series(self):
        # print(self.stock.price_history)
        self.assertTrue(len(self.stock.price_history) > 11)

    def test_should_calculate_crossover(self):
        t = self.timeseries.calculate_crossover(date.today())
        print('signal, (short series), (long series) >>> ', t)

    def tearDown(self):
        print(self.stock) if self.stock.price is not None else None
        print(self.timeseries) if self.stock.price is not None else None
        print('\n')
        del self.timeseries

    @classmethod
    def tearDownClass(cls):
        del cls.stock


class StockDMACspot(StockDMACscenario):
    """Test time series and DMAC analysis' methods in single test cases"""
    @classmethod
    def setUpClass(cls):
        cls.stock = Stock("GOOG")

    def setUp(self):
        # create a simpler price history
        self.trend_fixture(
            [82, 79, 84.1, 85.6, 80.9, 81.2, 81.5, 81.7, 82.0, 82.2, 82.5]
        )
        # create a DMAC object for the stock
        self.timeseries = TimeSeries(self.stock)

    def test_should_create_time_series(self):
        # print(self.stock.price_history)
        self.assertTrue(len(self.stock.price_history) > 10)

    def test_should_raise_error_in_calculate_stma(self):
        with self.assertRaises(ValueError):
            self.timeseries.calculate_stma_ltma(date.today(), period='abc')
            self.timeseries.calculate_stma_ltma(date.today(), period=1)

    def test_should_calculate_stma(self):
        stma = self.timeseries.calculate_stma_ltma(date.today(), period='short')
        print('STMA: ', stma)
        self.assertAlmostEqual(stma, 82.16, delta=0.0001)

    def test_should_calculate_ltma(self):
        ltma = self.timeseries.calculate_stma_ltma(date.today(), period='long')
        print('LTMA: ', ltma)
        self.assertAlmostEqual(ltma, 82.07, delta=0.0001)

    def test_should_calculate_crossover(self):
        t = self.timeseries.calculate_crossover(date.today())
        print('signal, (short series), (long series) >>> ', t)
        self.assertEqual(t[0], 0)

    def tearDown(self):
        del self.timeseries

    @classmethod
    def tearDownClass(cls):
        del cls.stock


if __name__ == "__main__":
    unittest.main()