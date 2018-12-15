from lxml import html
from collections import OrderedDict
from time import sleep
from os import listdir
from os.path import isfile, join
import requests
import json
import inspect
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

all_stocks = [
           ('3M', 'MMM'),
           ('Academedia', 'ACAD.ST'),
           ('Acando', 'ACAN-B.ST'),
           ('Activision Blizzard Inc', 'ATVI'),
           ('Alibaba Group Holding Ltd', 'BABA'),
           ('Alphabet Inc Class A', 'GOOGL'),
           ('Amazon.com Inc', 'AMZN'),
           ('Arista Networks Inc', 'ANET'),
           ('Assa Abloy B', 'ASSA-B.ST'),
           ('AstraZeneca', 'AZN.ST'),
           ('Atlas Copco B', 'ATCO-B.ST'),
           ('Atlassian Corp PLC', 'TEAM'),
           ('Autoliv SDB', 'ALIV-SDB.ST'),
           ('Berkshire Hathaway Inc Class B', 'BRK.B'),
           ('Boliden', 'BOL.ST'),
           ('Booking Holding', 'BKNG'),
           ('Bure Equity', 'BURE.ST'),
           ('C-RAD B', 'CRAD-B.ST'),
           ('Castellum', 'CAST.ST'),
           ('CellaVision ', 'CEVI.ST'),
           ('Cirrus Logic Inc', 'CRUS'),
           ('Climeon B', 'CLIME-B.ST'),
           ('Epiroc B', 'EPI-B.ST'),
           ('Essity B', 'ESSITY-B.ST'),
           ('Fortinet Inc', 'FTNT'),
           ('Handelsbanken A', 'SHB-A.ST'),
           ('Hansa Medical', 'HMED.ST'),
           ('Heliospectra', 'HELIO.ST'),
           ('Hexagon B', 'HEXA-B.ST'),
           ('Hexpol B', 'HPOL-B.ST'),
           ('Intuitive Surgical Inc', 'ISRG'),
           ('Investor A', 'INVE-A.ST'),
           ('Investor B', 'INVE-B.ST'),
           ('JD.com Inc', 'JD'),
           ('Johnson & Johnson', 'JNJ'),
           ('Kindered Group', 'KIND-SDB.ST'),
           ('Knowit', 'KNOW.ST'),
           ('Latour B', 'LATO-B.ST'),
           ('Lundbergsföretagen B', 'LUND-B.ST'),
           ('Markel Corp', 'MKL'),
           ('Masimo Corporation', 'MASI'),
           ('Match Group', 'MTCH'),
           ('Netflix', 'NFLX'),
           ('Nio', 'NIO'),
           ('Nobina', 'NOBINA.ST'),
           ('Novo Nordisk', 'NOVO-B.CO'),
           ('PayPal Holding Inc', 'PYPL'),
           ('Peab B', 'PEAB-B.ST'),
           ('PowerCell Sweden', 'PCELL.ST'),
           ('Proact IT Group', 'PACT.ST'),
           ('Probi', 'PROB.ST'),
           ('Proofpoint inc', 'PFPT'),
           ('RaySearch Laboratories B', 'RAY-B.ST'),
           ('Sandvik', 'SAND.ST'),
           ('SCA B', 'SCA-B.ST'),
           ('SEB A', 'SEB-A.ST'),
           ('Service Corporation International', 'SCI'),
           ('Star Group Inc', 'TSGI.TO'),
           ('SWECO B', 'SWEC-B.ST'),
           ('Swedish Orphan Biovitrum', 'SOBI.ST'),
           ('Tesla Inc', 'TSLA'),
           ('Veoneer SDB', 'VNE-SDB.ST'),
           ('Vicore Pharma Holding', 'VICO.ST'),
           ('Victoria Park B', 'VICP-B.ST'),
           ('Walt Disney CO', 'DIS'),
           ('Zillow Group Inc Class A Share', 'ZG'),
           ]

store_result_fldr = 'tickers'
root_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

if not os.path.exists(store_result_fldr):
    os.makedirs(store_result_fldr)


# http://www.nasdaqomxnordic.com/aktier
# https://finance.yahoo.com/quote/ASSA-B.ST/history?p=ASSA-B.ST
def parse(ticker):
    url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    response = requests.get(url, verify=False)
    print("Parsing %s" % url)
    sleep(4)
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)
    try:
        json_loaded_summary = json.loads(summary_json_response.text)
        y_target_est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        datelist = []
        for i in earnings_list['earningsDate']:
            datelist.append(i['fmt'])
        earnings_date = ' to '.join(datelist)
        for table_data in summary_table:
            raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            summary_data.update({table_key: table_value})
        summary_data.update({'1y Target Est': y_target_est, 'EPS (TTM)': eps, 'Earnings Date': earnings_date, 'ticker': ticker, 'url': url})
        return summary_data
    except:
        print("Failed to parse json response")
        return {"error": "Failed to parse json response"}


def load_all_tickers(tickers):
    '''
    Gets the latest info of the tickers.

    :param tickers: array of tuples
    :return: void
    '''

    # TODO: add time calculation
    # TODO: add error handling if scraping fails...this is also done in json file.
    # TODO: add counter that counts all parsing, example: 53 of 55 read ok, 2 failed.
    # TODO: add unit tests on the implementation
    # TODO: fix errors in printout HTTPS READ...

    for ticker in tickers:
        tick = ticker[1]
        print("Fetching data for %s - %s" % (ticker[1], ticker[0]))
        scraped_data = parse(tick)
        path_to_file = os.path.join(root_dir, store_result_fldr, '%s-summary.json')
        with open(path_to_file % tick, 'w') as fp:
            json.dump(scraped_data, fp, indent=4)


def load_historical_data(tickers, from_date, to_date):
    '''
    Gets all historical data of the tickers.
    :return:
    '''
    # or create scv files locally

    # om vi har historisk data i csv, vi vill bara lägga på den senaste infon sist i csv file.
    # alt. läsa in det i databas.

    pass


def get_all_json_in_ticker():
    path_to_file = os.path.join(root_dir, store_result_fldr)
    return [os.path.join(path_to_file, file_in_dir) for file_in_dir in listdir(path_to_file) if isfile(join(path_to_file, file_in_dir))]


def get_json_in_file(path_to_file):
    with open(path_to_file) as file:
        return json.load(file)


def scan_files_for_errors():
    for file in get_all_json_in_ticker():
        # json_load = json.loads(get_json_in_file(file))
        json_load = get_json_in_file(file)
        # print("json_load[""error""]%s: " % json_load["error"])
        error_value = json_load.get('error')
        if error_value is not None:
            print("error found in file: %s, %s" % (file, json_load.get('error')))



# create web page for showing if stock is going up or down.
# https://www.youtube.com/watch?v=sXyXciMYZZw



if __name__=="__main__":
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('ticker',help = '')
    # args = argparser.parse_args()
    # ticker = args.ticker

    # load_all_tickers(all_stocks)
    load_all_tickers(
        [
         ('Atlas Copco AB', 'ATCO-B.ST'),
         ('Berkshire Hathaway Inc Class B', 'BRK.B'),
         ('C-RAD B', 'CRAD-B.ST'),
         ('Investor A', 'INVE-A.ST'),
         ]
    )

    # for f in get_all_json_in_ticker():
    #    print(str(f))

    scan_files_for_errors()



