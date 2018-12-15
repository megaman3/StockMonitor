import unittest
import scrape_usa_stock_data
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestScrapeStockData(unittest.TestCase):

    error_tickers = [
         ('Atlas Copco AB', 'ATCO-B.ST'),
         ('Berkshire Hathaway Inc Class B', 'BRK.B'),
         ('C-RAD B', 'CRAD-B.ST'),
         ('Investor A', 'INVE-A.ST'),
         ]

    def test_parse(self):
        scrape_usa_stock_data.load_all_tickers(self.error_tickers)
        scrape_usa_stock_data.scan_files_for_errors()


if __name__ == '__main__':
    unittest.main()
