from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo
from tqdm import tqdm
from dotenv import dotenv_values
import requests
import datetime

filteredList = []
def filterTickers(tickersList, listName):
    # with open("monthlyOptionTickers.txt") as file:
    #     for line in file:
    #         excludedTickers = line.split(',')
    # file.close()

    for ticker in tqdm(tickersList, desc = "Filtering 'big'" if listName=='big_filtered' else "Filtering '20-100'"):
        data = callApi(ticker)
        if (data['status'] == "FAILED"): # Closest friday had no options, hence failed
                pass
        else:
            # Add to filtered list
            filteredList.append(ticker)

    return filteredList

# Get nearest friday 
toDate = datetime.datetime.now()
toDate = toDate + datetime.timedelta( (4-toDate.weekday()) % 7 )
toDate = toDate.strftime("%Y-%m-%d")

try:
     apiKey = dotenv_values(".env")["apikey"]
except:
      raise Exception("No key found.  Did you set your .env file?  Refer to .env.template for instructions")      

@on_exception(expo, requests.exceptions.RequestException, max_time=60)
@sleep_and_retry
@limits(calls=120, period=60)
def callApi(ticker):
    url = f"https://api.tdameritrade.com/v1/marketdata/chains?apikey={apiKey}&symbol={ticker}&strikeCount=1&fromDate=2022-01-01&toDate={toDate}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    if list(data.keys())[0] == "error":
        #print("Reached max on: " + ticker[0] + ".  Trying again...")
        raise requests.exceptions.RequestException

    return data