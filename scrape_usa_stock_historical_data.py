from lxml import html
from collections import OrderedDict

from time import sleep
import time

import numpy as np
import fix_yahoo_finance as yf
import datetime

from os import listdir
from os.path import isfile, join
import requests
import json
import inspect
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


curr = time.strftime("%Y-%m-%d")
yr_diff = datetime.datetime.now() - datetime.timedelta(days=3*365)
yr_diff = yr_diff.strftime("%Y-%m-%d")
ibm = yf.download("IBM", start=yr_diff, end=curr)
sp500 = yf.download("^GSPC", start=yr_diff, end=curr)

# print("ibm: " + str(ibm))
print("sp500: " + str(sp500))
# print("ibm: " + str(ibm['Close'].values))

# TODO:
# store on GIT
# save historical data locally
# create an engine that scan for trends, # days in negative trend, value down and maybe delta and give me a notification on that, maybe an email.
# deploy in aws or google cloud.
# add SMA 200, RSI etc...and create warnings signal on that.
# maybe create gui, and a web page.

