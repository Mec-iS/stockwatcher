# coding=utf-8
import bisect

__author__ = 'Lorenzo'

# #todo: implement DMAC
# #todo: implement TimeSeries
# #todo: implement moving average


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        # list of tuples list[0] is most recent
        self.price_history = []

    def __repr__(self):
        return 'Stock: {name!r} is {id!r}'.format(
            name=self.symbol,
            id=id(self)
        )

    def __str__(self):
        return 'Stock {name!s}, its current price is {price!s}'.format(
            name=self.symbol,
            price=self.price
        )

    @property
    def price(self):
        return self.price_history[-1][1] if self.price_history else None

    def update(self, timestamp, price):
        """Update price"""
        if not price > 0:
            raise ValueError('Price must be non-zero positive')
        # order updates from most recent, handles late updates
        # #todo: [DONE] implemented bisect module
        return bisect.insort_left(
            self.price_history, (timestamp, price, )
        ) if (timestamp, price, ) not in self.price_history else ValueError(
            'Update already in price history'
        )

    @property
    def trend(self):
        """Return a trend (the last three prices)"""
        # take the last 3 elements and reverse them, return list of prices
        return [p[1] for p in self.price_history[-3:]]

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
            for i in range(len(t)-1)
        )
        if all(gen) is True:
            return True
        elif all(gen) is False:
            return False
        else:
            return None

