# coding=utf-8
from datetime import datetime, timedelta, date
from collections import namedtuple

__author__ = 'Lorenzo'

# Create a named tuple to represent price updates in the history
Update = namedtuple('Update', ['timestamp', 'price'])


class TimeSeries:
    """Provide time series and DMAC analysis"""
    def __init__(self, stock):
        # Turn tuples in to namedtuples for better handling
        self.symbol = stock.symbol
        self.history = [
            Update(
                timestamp=p[0],
                price=p[1]
            )
            for p in stock.price_history
        ]

    def __repr__(self):
        return 'Time series for {name!r} is {id!r}'.format(
            name=self.symbol,
            id=id(self)
        )

    def __str__(self):
        return ('Time series for {name!s}: {series!s}. \nAt {date!s} its STMA is {stma!s} and its '
                'LTMA is {ltma!s}').format(
            name=self.symbol,
            series= [('{:%Y-%m-%d %H:%M:%S}'.format(p.timestamp), p.price) for p in self.history],
            date=date.today(),
            stma=self.calculate_stma_ltma(date.today(), 'short'),
            ltma=self.calculate_stma_ltma(date.today(), 'long'),
        )

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
        # #todo: return short and long average in the same return statement (short, long)
        # #todo: or (short, 0) or (0,0) if not enough prices in history
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
        return round((sum(series) / len(series)), 8)

    def calculate_crossover(self, on_date):
        """
        Calculate if there is a crossover in a given date, if yes
        a signal to buy (1), sell (-1) or neutral (0) is returned.

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

        :param date on_date:
        :return: tuple(int, tuple, tuple)
        """
        # #todo: refactor when self.calculate_stma_ltma() is refactored

        # calculate short series for the given date and the date before
        s_series = [
            (
                self.calculate_stma_ltma(
                    self.history[self.history.index(d)-2].timestamp, 'short'
                ),
                self.calculate_stma_ltma(
                    self.history[self.history.index(d)-1].timestamp, 'short'
                ),
                self.calculate_stma_ltma(
                    d.timestamp, 'short'
                ),
             )
            for d in self.history
            if d.timestamp == on_date
        ][0]
        # calculate long series for the given date and the date before
        l_series = [
            (
                self.calculate_stma_ltma(
                    self.history[self.history.index(d)-2].timestamp, 'long'
                ),
                self.calculate_stma_ltma(
                    self.history[self.history.index(d)-1].timestamp, 'long'
                ),
                self.calculate_stma_ltma(
                    d.timestamp, 'long'
                ),
             )
            for d in self.history
            if d.timestamp == on_date
        ][0]
        # check if there is crossover in the given date
        if abs(s_series[2] - l_series[2]) <= 0.02:
            # check s_series for days before for signal
            if s_series[0] >= l_series[0]:
                # sell signal
                return -1, s_series, l_series
            elif s_series[0] < l_series[0]:
                # buy signal
                return 1, s_series, l_series
        # no crossover or neutral signal
        return 0, s_series, l_series

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
        """def calculate(date, series=[]):
            if date == on_date:
                return series

            return calculate(date, series)

        return tuple()"""
        raise NotImplemented()

