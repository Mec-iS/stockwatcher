# coding=utf-8
from datetime import datetime, timedelta
from collections import namedtuple

__author__ = 'Lorenzo'

# Create a named tuple to represent price updates in the history
Update = namedtuple('Update', ['timestamp', 'price'])


class TimeSeries():
    """Provide time series and DMAC analysis"""
    def __init__(self, stock):
        # Turn tuples in to namedtuples for better handling
        self.history = [
            Update(
                timestamp=p[0],
                price=p[1]
            )
            for p in stock.price_history
        ]

    def calculate_stma_ltma(self, on_date, period='short'):
        """
        Calculate the average price of the previous 5 or 10 days from
        the given date.

        Example:
           >>> # calculate STMA
           >>> calculate_stma_ltma(date.today(), 'short')
           >>> # calculate LTMA
           >>> calculate_stma_ltma(date.today(), 'long')


        :param date on_date: the reference date, default is 5
        :param str period: 'short' for STMA, 'long' for LTMA. Default: 'short'
        :return: float
        """
        period = {
            'short': 5,
            'long': 10
        }.get(period)
        if period is None: raise ValueError('period can be only \'short\' or \'long\'')

        # #todo: consider only closing prices
        series = [
            h.price
            for h in self.history
            if on_date - timedelta(period) <= h.timestamp < on_date
        ]
        return sum(series) / len(series)


    def calculate_stma_ltma_time_series(self, on_date, delta):
        """
        Calculate the time series of the Short Term Moving Average.
        Return the STMA for the five days before the given date.
        Calculate STMA recursevely for the last give number of days.


        :param date on_date:
        :param int delta:
        :return:
        """
        # slice price_history for the last five closing price
        # reverse
        #
        raise NotImplemented()
        """def calculate(date, series=[]):
            if date == on_date:
                return series

            return calculate(date, series)

        return tuple()"""


    def get_crossover_signal(self, on_date):
        """
        Check if in a given date there is a buy/sell signal using DMAC analysis.

        Documentation:
            Consider a stock, with closing prices as shown above. First, we
            calculate two moving average trends. The short-term (5-day) moving
            (STMA) average is calculated by taking the moving average for a
            short number of days. The long-term moving (LTMA) average is
            calculated by taking the moving average for a longer number of days,
            for example the moving average of the last 10 days.
            If the STMA crosses below-to-above the LTMA, that is a buy signal.
            If the STMA crosses above-to-below the LTMA, that is a sell signal.

        :param datetime date:
        :return: 1, -1, 0
        """
        stm_lower = on_date - timedelta(6)
        ltm_lower = on_date -timedelta(11)
