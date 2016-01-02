# coding=utf-8
import unittest

__author__ = 'Lorenzo'

from stock import Stock
from datetime import datetime


class StockTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.stock = Stock("GOOG")

    def trend_fixture(self, prices):
        """Create three new price in price history from a list of Float.
    To be used in the tests below."""
        return [self.stock.update(datetime(2015, 12, i+1), price=p)
                for i, p in enumerate(prices)]

    def test_should_create_Stock_object(self):
        self.assertIsInstance(self.stock, Stock)

        self.assertRaises(
            ValueError,
            self.trend_fixture,
            [80, -78.3, 81.1]
        )

    def test_price_of_a_new_stock_class_should_be_None(self):
        self.assertIsNone(self.stock.price)

    def test_should_update_price(self):
        """Requirement: * Price has to update properly via a `update` method, with a
    timestamp also"
        """
        self.stock.update(datetime(2015, 12, 5), price=80)
        self.assertEqual(self.stock.price, 80)

    def test_negative_price_should_raise_valuerror(self):
        """Requirement: * Price cannot be negative"""
        # assertRaise returns a context! Cool
        with self.assertRaises(ValueError):
            self.stock.update(datetime(2015, 12, 5), -1)

    def test_after_multiple_updates_should_return_ordered(self):
        """Requirement: * After multiple updates, elements in stock.price_history
    should be ordered from the latest to the oldest"""
        self.stock.update(datetime(2015, 12, 5), price=80)
        self.stock.update(datetime(2015, 12, 6), price=82.6)
        self.stock.update(datetime(2015, 12, 4), price=81)
        self.stock.update(datetime(2015, 12, 9), price=87.6)
        self.stock.update(datetime(2015, 12, 7), price=81.9)
        self.stock.update(datetime(2015, 12, 8), price=84.9)

        self.assertEqual(
            [s[1] for s in self.stock.price_history],
            [87.6, 84.9, 81.9, 82.6, 80, 81]
        )

    def test_after_multiple_updates_should_return_last(self):
        """Requirement: * After multiple updates, stock.price gives us the latest
    price"""
        self.stock.update(datetime(2015, 12, 5), price=80)
        self.stock.update(datetime(2015, 12, 6), price=82.6)
        self.stock.update(datetime(2015, 12, 4), price=81)
        self.stock.update(datetime(2015, 12, 9), price=87.6)
        self.stock.update(datetime(2015, 12, 7), price=81.9)
        self.stock.update(datetime(2015, 12, 8), price=84.9)

        self.assertAlmostEqual(self.stock.price, 87.6, delta=0.1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


class StockTrendTest(StockTest):
    """Requirement: * implement a method to check if a a stock has a incremental
trend (if the last three quotes are increasing)"""
    @classmethod
    def setUpClass(cls):
        pass

    # inherit setUp() from super()

    def test_trend_should_return_last_three_prices(self):
        """Test the stock.trend method"""
        self.trend_fixture([82, 79, 80, 78.3, 81.1])
        self.assertTrue(self.stock.trend, [80, 78.3, 81.1])
        print('Stock.trend returns the last three prices')

    def test_trend_should_be_incremental(self):
        """Pass three recent growing prices in the method"""
        self.trend_fixture([82, 79, 81.1, 82.6, 84.9])
        self.assertTrue(self.stock.trend_is_incremental())

    def test_trend_should_be_decremental(self):
        """Pass three recent decrementing prices in the method"""
        self.trend_fixture([82, 79, 84.1, 82.6, 80.9])
        self.assertFalse(self.stock.trend_is_incremental())

    def test_trend_should_be_none(self):
        """Pass three recent not trended prices in the method"""
        self.trend_fixture([82, 79, 84.1, 85.6, 80.9])
        self.assertIsNone(self.stock.trend_is_incremental())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
