# coding=utf-8
import unittest

__author__ = 'Lorenzo'

from stock import Stock
from rules import Rule
from datetime import datetime


class RuleTest(unittest.TestCase):
    """
    Requirements:
       * Rules should accept a Stock and a condition
       * Rules should trigger some event if condition is met
    """
    @classmethod
    def setUpClass(cls):
        cls.stock = Stock("GOOG")
        cls.stock.update(datetime(2015, 12, 5), price=80)
        cls.exchange = {
            cls.stock.symbol: cls.stock
        }

    def setUp(self):
        pass

    def test_should_create_a_rule(self):
        rule = Rule(self.stock, lambda stock: self.stock.price > 79.8)
        self.assertEqual(rule.stock.price, 80)
        self.assertTrue(callable(rule.condition))
        print(rule.condition(self.stock), ' stock.price is higher than 79.8')

    def test_should_fail_create_a_rule(self):
        self.assertRaises(
            TypeError,
            Rule(
                self.stock.symbol,
                lambda stock: self.stock.price > 79.8
            )
        )
        self.assertRaises(
            TypeError,
            Rule(
                self.stock,
                'stock price > 79.8'
            )
        )

    def test_check_condition_should_be_True(self):
        rule = Rule(self.stock, lambda stock: self.stock.price > 79.8)
        self.assertTrue(rule.check_condition)

    def test_check_condition_should_be_False(self):
        rule = Rule(self.stock, lambda stock: self.stock.price > 92)
        self.assertFalse(rule.check_condition)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()