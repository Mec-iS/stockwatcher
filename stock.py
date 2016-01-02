# coding=utf-8
__author__ = 'Lorenzo'


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        # list of tuples list[0] is most recent
        self.price_history = []

    def update(self, timestamp, price):
        """Update price"""
        if not price > 0:
            raise ValueError('Price must be non-zero positive')
        price_history = self.price_history + [(timestamp, price, )]
        # order updates from most recent, handles late updates
        return setattr(
            self,
            'price_history',
            sorted(price_history, key=lambda x: x[0], reverse=True)
        )

    @property
    def trend(self):
        """Return a trend (the last three prices)"""
        # take the last 3 elements and reverse them, return list of prices
        return [p[1] for p in self.price_history[:2]]

    def trend_is_incremental(self):
        """Return:
         * True: the last three prices are growing
         * False: the last three prices are shrinking
         * None: none of the above"""
        t = self.trend
        gen = (
            True
            if t[i] > t[i+1]
            else False
            for i in range(len(t)-1)
        )
        if all(gen) is True:
            return True
        elif all(gen) is False:
            return False
        else:
            return None

    @property
    def price(self):
        return self.price_history[0][1] if self.price_history else None
