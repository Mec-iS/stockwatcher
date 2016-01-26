# coding=utf-8
import unittest

__author__ = 'Lorenzo'

from src.event import Event


class EventTest(unittest.TestCase):
    def test_a_listener_is_notified_when_an_event_is_raised(self):
        called = False

        def listener():
            nonlocal called
            called = True

        event = Event()
        event.connect(listener)
        event.fire()
        self.assertTrue(called)

if __name__ == '__main__':
    unittest.main()
