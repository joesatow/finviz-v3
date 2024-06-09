from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo
from tqdm import tqdm
from dotenv import dotenv_values
import datetime
import requests
import pytz
import os
import json

local_tz = pytz.timezone('America/New_York')

filename = "excludedTickers.txt"
if not os.path.exists(filename):
    file = open(filename,"w")
    file.write('FIRST')
    file.close()

file = open(filename,"r")
excludedTickers = file.read().split(',')
file.close()

file = open("goodTickers.txt","r")
goodTickers = file.read().split(',')
file.close()

def filterTickers(tickersList, listName):
    filteredList = []

    file = open(filename,"a")
    for ticker in tqdm(tickersList, desc = "Filtering 'big'" if listName=='big_filtered' else "Filtering '20-100'"):
        if ticker in excludedTickers:
            continue
        if ticker not in goodTickers:
            continue
        else:
            # Add to filtered list
            filteredList.append(ticker)
    file.close()
    
    return filteredList