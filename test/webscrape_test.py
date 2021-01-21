import unittest
from src.webscrape import YahooWebScrapeInstance
from src.webscrape import YahooWebScrapeException
import pandas as pd


class WebScrapeTest(unittest.TestCase):
    def test_RequestExceptions(self):
        """
        Testcase for Instantiation Exceptions that can arise from unwanted responses to requests
        """
        with self.assertRaises(YahooWebScrapeException):
            YahooWebScrapeInstance('')
        with self.assertRaises(YahooWebScrapeException):
            YahooWebScrapeInstance('123')
        with self.assertRaises(YahooWebScrapeException):
            YahooWebScrapeInstance('asdf')

    def test_IndexError(self):
        """
        Testcase for testing the index error that can be created for days back function
        """
        try:
            instance = YahooWebScrapeInstance('ISRG')
            self.assertEqual(str, type(instance.get_days_back(0)))
            self.assertEqual(pd.DataFrame, type(instance.dataframe_table))
        except YahooWebScrapeException as ywse:
            self.fail(ywse.default_msg)

        with self.assertRaises(IndexError):
            instance.get_days_back(-1)
        with self.assertRaises(IndexError):
            instance.get_days_back(100)

    def test_Successful(self):
        """
        Test that basic instantiation and functions are working as intended
        Testing that instantiation with lowercase and uppercase don't matter and that responses/instantiation are consistent
        """
        try:
            instance1 = YahooWebScrapeInstance('ISRG')
            self.assertEqual("ISRG", instance1.symbol)
            self.assertEqual(100, len(instance1.dataframe_table.index))
            self.assertEqual(pd.DataFrame, type(instance1.dataframe_table))
            self.assertEqual(str, type(instance1.get_days_back(0)))
            instance2 = YahooWebScrapeInstance('isrg')
            self.assertEqual("ISRG", instance2.symbol)
            self.assertEqual(100, len(instance2.dataframe_table.index))
            self.assertEqual(pd.DataFrame, type(instance2.dataframe_table))
            self.assertEqual(str, type(instance2.get_days_back(0)))

            self.assertEqual(instance1.symbol, instance2.symbol)
            self.assertEqual(instance1.dataframe_table.columns.all(), instance2.dataframe_table.columns.all())
            self.assertEqual(list(instance1.dataframe_table['Date']), list(instance2.dataframe_table['Date']))
            self.assertEqual(list(instance1.dataframe_table['Open']), list(instance2.dataframe_table['Open']))
            self.assertEqual(list(instance1.dataframe_table['High']), list(instance2.dataframe_table['High']))
            self.assertEqual(list(instance1.dataframe_table['Low']), list(instance2.dataframe_table['Low']))
            self.assertEqual(list(instance1.dataframe_table['Close*']), list(instance2.dataframe_table['Close*']))
            self.assertEqual(list(instance1.dataframe_table['Adj Close**']), list(instance2.dataframe_table['Adj Close**']))
            self.assertEqual(list(instance1.dataframe_table['Volume']), list(instance2.dataframe_table['Volume']))
            self.assertEqual(instance1.get_days_back(0), instance2.get_days_back(0))
        except YahooWebScrapeException as ywse:
            self.fail(ywse.default_msg)
        except IndexError as ie:
            self.fail("Index Error in get_days_back" + str(ie))


if __name__ == '__main__':
    unittest.main()
