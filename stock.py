# coding=utf-8
__author__ = 'Lorenzo'


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []   # list of tuples

    def update(self, timestamp, price):
        """Update price"""
        if not price > 0:
            raise ValueError('Price must be non-zero positive')
        return self.price_history.append((timestamp, price, ))

    @property
    def trend(self):
        """Return a trend (the last three prices)"""
        # take the last 3 elements and reverse them, return list of prices
        return [p[1] for p in self.price_history[-3:][:]]

    def trend_is_incremental(self):
        """Return:
         * True: the last three prices are growing
         * False: the last three prices are shrinking
         * None: none of the above"""
        t = self.trend
        gen = (
            True
            if t[i] < t[i+1]
            else False
            for i in range(len(t)) if i != 2
        )
        if all(gen) is True:
            return True
        elif all(gen) is False:
            return False
        else:
            return None

    @property
    def price(self):
        return self.price_history[-1][1] if self.price_history else None
