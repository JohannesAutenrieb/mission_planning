from unittest import TestCase
from src import DataHandler
import time


class DataHandlerTest(TestCase):

    def setUp(self):
        self.handler = DataHandler()

    def test_get_foo_data(self):

        fooPackage = []

        fooPackage.append([1, [52.06922871, -0.62585592, 5.02500000], time.time()])
        fooPackage.append([2, [52.06904404, -0.62584519, 4.19575000], time.time()])
        fooPackage.append([3, [52.06879343, -0.62585592, 52.06879343], time.time()])

        # Verify if lists are created properly
        self.handler.get_foo_data(fooPackage)
        self.assertListEqual([1, 2, 3], self.handler.fooId)
        self.assertListEqual([[52.06922871, -0.62585592, 5.02500000], [52.06904404, -0.62584519, 4.19575000],
                              [52.06879343, -0.62585592, 52.06879343]], self.handler.fooPos)
        self.assertListEqual(fooPackage[0][2], self.handler.fooTimestamp)