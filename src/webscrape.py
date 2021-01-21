import requests
from bs4 import BeautifulSoup
from collections import deque
import pandas as pd
import numpy as np


class YahooWebScrapeInstance:
    """
    An Instance of a webscrape of recent prices of a given stock symbol

    Ex: YahooWebScrapeInstance('ISRG')
    """

    def __init__(self, stock_symbol):
        self.symbol = str(stock_symbol).upper()
        self.url = self.__build_url(self.symbol)
        self.dataframe_table = None  # Initialize dataframe as None
        self.dataframe_table, self.footnotes = self.process_response(self.url)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

    @staticmethod
    def __build_url(stock_symbol):
        """
        simple "private" method to build the url to get stock price history of a given stock symbol

        :param stock_symbol: the stock symbol for a corresponding company ('ISRG' is Intuitive Surgical)
        :return: the url for the corresponding stock symbol's price history from yahoo
        """
        return 'https://finance.yahoo.com/quote/' + str(stock_symbol) + '/history?p=' + str(stock_symbol)

    def process_response(self, url):
        """
        Processes the html response from the given url

        :param url:  yahoo stock history url link
        :return: DataFrame of the recent stock prices for the given url (which corresponds to a stock symbol)
        """
        try:
            html_response = requests.get(url)
        except requests.HTTPError as he:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(he))
        except requests.URLRequired as ur:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(ur))
        except requests.TooManyRedirects as tmr:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(tmr))
        except requests.ConnectTimeout as ct:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(ct))
        except requests.ConnectionError as ce:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(ce))
        except requests.ReadTimeout as rt:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(rt))
        except requests.Timeout as t:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(t))
        except requests.RequestException as re:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(re))

        if html_response.status_code == 404:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg="404 Response: Page Not Found.",
                                          status_code=html_response.status_code)
        elif html_response.status_code >= 500:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(html_response.status_code)
                                                                        + " Response: Server Error.  Returned content: "
                                                                        + str(html_response.content),
                                          status_code=html_response.status_code)
        elif html_response.status_code >= 400:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(html_response.status_code)
                                                                        + " Response: Client Error.  Returned content: "
                                                                        + str(html_response.content),
                                          status_code=html_response.status_code)
        elif html_response.status_code != 200:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str(html_response.status_code)
                                                                        + " Response.  Returned content: "
                                                                        + str(html_response.content),
                                          status_code=html_response.status_code)

        html_result = html_response.content
        soup = BeautifulSoup(html_result, 'html.parser')
        html_datatable = soup.find(class_="W(100%) M(0)")  # the name of the table class
        if html_datatable is None:
            raise YahooWebScrapeException(stock_symbol=self.symbol, msg=str("Symbol does not exist."), status_code=-1)
        try:
            table_elems = html_datatable.find_all('span')  # html element in the table class
            table_list = deque()
            for te in table_elems:
                if te.text != "Stock Split":  # Account for cases where stock split is in table (example with TSLA)
                    table_list.append(str(te.text))
                else:
                    table_list.pop()
            cols = list(table_list)[0:7]  # First seven entries are the column names
            for i in range(7):  # remove the first seven entries
                table_list.popleft()
            footnotes = []
            for i in range(3):  # remove last three entries (which correspond to some additional footnotes)
                footnotes.append(table_list.pop())
            footnotes.reverse()
            footnotes.pop()
            date_list = []
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            adj_close_list = []
            vol_list = []
            for i in range(int(len(table_list) / 7)):
                date_list.append(table_list.popleft())
                open_list.append(table_list.popleft())
                high_list.append(table_list.popleft())
                low_list.append(table_list.popleft())
                close_list.append(table_list.popleft())
                adj_close_list.append(table_list.popleft())
                vol_list.append(table_list.popleft())
            dataframe_table = pd.DataFrame(np.array([date_list, open_list, high_list, low_list, close_list,
                                                     adj_close_list, vol_list]).transpose())
            dataframe_table.columns = cols
        except Exception as e:
            raise YahooWebScrapeException(msg="Unexpected Exception: " + str(e))
        if len(dataframe_table.index) == 0:
            raise YahooWebScrapeException(stock_symbol=self.symbol,
                                          msg="Either invalid stock symbol or no information available",
                                          status_code=-1)
        return dataframe_table, "".join(footnotes)

    def get_days_back(self, days_back):
        """
        Returns the i row of the dataframe for this instance where i = days_back

        :param days_back: Number of days back that to retrieve the stock price information for this instance
        :return: the stock price information for this instance i market days ago where i = days_back;
        """
        if self.dataframe_table is not None:
            if len(self.dataframe_table.index) - 1 >= days_back >= 0:
                return str(self.dataframe_table.iloc[[days_back]]) + "\n" + str(self.footnotes) + "\n"
            else:
                raise IndexError
        return None


class YahooWebScrapeException(Exception):
    """
    Custom exception for this Yahoo WebScraping tool
    """

    def __init__(self, stock_symbol=None, msg=None, status_code=None):
        if msg is None:
            if stock_symbol is None:
                self.default_msg = "An error occurred while webscraping."
            else:
                self.default_msg = "An error occurred while webscraping this symbol: " + str(stock_symbol)
        else:
            if stock_symbol is None:
                self.default_msg = "An error occurred while webscraping.  " + str(msg)
            else:
                self.default_msg = "An error occurred while webscraping this symbol: " + str(stock_symbol) + ".  " + \
                                   str(msg)
        self.status_code = status_code
