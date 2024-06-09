from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo
from tqdm import tqdm
from scripts_jserver import get_access_token
import datetime
import requests
import pytz

# This script checks my big list of optionable stocks and verfies that they meet two criteria:
#   1. They have friday options
#   2. They don't have earnings in the next 2 weeks
# 
# If they 

symbolsList = ['MMM', 'ABT', 'ABBV', 'ANF', 'ASO', 'ACAD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AFRM', 'AFL', 'ABNB', 'AKAM', 'AA', 'BABA', 'ALGN', 'GOOGL', 'GOOG', 'AMLP', 'MO', 'AMZN', 'AMBA', 'AXP', 'AIG', 'ABC', 'AMGN', 'ADI', 'BUD', 'NLY', 'AR', 'APA', 'APO', 'AAPL', 'AMAT', 'MT', 'ADM', 'ANET', 'ARKF', 'ARKG', 'ARKK', 'ASML', 'AZN', 'T', 'TEAM', 'ADSK', 'ADP', 'AZO', 'CAR', 'BIDU', 'BK', 'VXX', 'BBWI', 'BAX', 'BDX', 'BRK.B', 'BBY', 'BILL', 'BIIB', 'BNTX', 'BAC', 'BLK', 'BX', 'SQ', 'BA', 'BKNG', 'BSX', 'BP', 'BMY', 'AVGO', 'BURL', 'CZR', 'CCJ', 'CPB', 'CWH', 'GOOS', 'CSIQ', 'COF', 'CPRI', 'CAH', 'CVNA', 'SAVA', 'CAT', 'CBOE', 'CNC', 'CF', 'CHTR', 'CC', 'CVX', 'CHWY', 'CMG', 'CI', 'CSCO', 'C', 'CLF', 'CLX', 'NET', 'CME', 'KO', 'COIN', 'CL', 'CMCSA', 'CAG', 'COP', 'STZ', 'CLR', 'GLW', 'COST', 'CTRA', 'COUP', 'CPNG', 'CRSP', 'CRWD', 'CSX', 'CVS', 'DHI', 'DHR', 'DDOG', 'PLAY', 'ASHR', 'DE', 'DAL', 'DVN', 'DKS', 'DWAC', 'FAZ', 'DUST', 'JNUG', 'LABD', 'TZA', 'YINN', 'ERX', 'FAS', 'NUGT', 'JDST', 'SOXS', 'TNA', 'DFS', 'DIS', 'DOCU', 'DG', 'DLTR', 'DPZ', 'DASH', 'DOW', 'DBX', 'DD', 'BROS', 'EBAY', 'EW', 'EA', 'ELV', 'EMR', 'ENVX', 'ENPH', 'EPD', 'EOG', 'EQT', 'JETS', 'ETSY', 'EXAS', 'EXPE', 'XOM', 'FFIV', 'FDX', 'RACE', 'FSLR', 'FISV', 'FIVE', 'FLR', 'FL', 'FOXA', 'FCX', 'FUTU', 'GME', 'GD', 'GE', 'GM', 'GILD', 'URA', 'GS', 'GSK', 'HAL', 'HOG', 'HIG', 'HLF', 'HSY', 'HES', 'HD', 'HON', 'HRL', 'HPQ', 'HSBC', 'HUM', 'ITW', 'ILMN', 'INTC', 'IBM', 'IP', 'INTU', 'ISRG', 'FXE', 'UUP', 'TAN', 'BKLN', 'QQQ', 'SARK', 'IRBT', 'IAU', 'EWZ', 'EWC', 'EWG', 'EWJ', 'EWW', 'EWY', 'SLV', 'TLT', 'IEF', 'FXI', 'IVV', 'ICLN', 'HYG', 'LQD', 'IBB', 'EMB', 'EFA', 'EEM', 'EWU', 'IWM', 'TIP', 'IYR', 'ITB', 'JD', 'JKS', 'JNJ', 'YY', 'JPM', 'JNPR', 'KMB', 'KMI', 'KKR', 'KLAC', 'KSS', 'KHC', 'KWEB', 'KR', 'LRCX', 'LVS', 'LMND', 'LEN', 'LI', 'LLY', 'LMT', 'LOW', 'LULU', 'LITE', 'M', 'MRO', 'MPC', 'MAR', 'MRVL', 'MA', 'MTCH', 'MAT', 'MCD', 'MCK', 'MDT', 'MELI', 'MRK', 'META', 'MET', 'MGM', 'MCHP', 'MU', 'MSFT', 'MSTR', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'MS', 'MOS', 'COOP', 'NCR', 'NTAP', 'NTES', 'NFLX', 'EDU', 'NEM', 'NKE', 'JWN', 'NSC', 'NOC', 'NOV', 'NVAX', 'NUE', 'NTNX', 'NTR', 'NVDA', 'NXPI', 'OXY', 'OKTA', 'OLN', 'ON', 'ORCL', 'OSTK', 'PANW', 'PARA', 'PYPL', 'PENN', 'PEP', 'PFE', 'PM', 'PSX', 'PDD', 'PINS', 'PXD', 'PLUG', 'PNC', 'PPG', 'PG', 'SVXY', 'UCO', 'VIXY', 'SSO', 'TBT', 'TQQQ', 'SQQQ', 'SDS', 'UPRO', 'QCOM', 'RRC', 'RTX', 'REGN', 'RH', 'RNG', 'RIVN', 'RBLX', 'ROKU', 'ROST', 'RCL', 'SPGI', 'CRM', 'SRPT', 'SLB', 'SCHW', 'SE', 'STX', 'XLC', 'XLE', 'XLF', 'XLY', 'XLP', 'XLV', 'XLI', 'XLU', 'XLB', 'XLK', 'NOW', 'SHOP', 'SIG', 'SKX', 'SWKS', 'SNOW', 'SONY', 'SO', 'LUV', 'DIA', 'GLD', 'FEZ', 'SPY', 'XBI', 'XHB', 'XME', 'XOP', 'KRE', 'XRT', 'SAVE', 'SPLK', 'SPOT', 'SBUX', 'SYK', 'SU', 'SPWR', 'SYF', 'SYY', 'TMUS', 'TSM', 'TTWO', 'TNDM', 'TPR', 'TGT', 'TECK', 'TDOC', 'THC', 'TSLA', 'TXN', 'TTD', 'TMO', 'TJX', 'TOL', 'MODG', 'TSCO', 'TRIP', 'TWLO', 'UBER', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'X', 'UNG', 'USO', 'UNH', 'U', 'OLED', 'UPST', 'URBN', 'USB', 'VFC', 'VLO', 'GDX', 'GDXJ', 'OIH', 'SMH', 'VZ', 'VRTX', 'V', 'WBA', 'WMT', 'WM', 'W', 'WFC', 'WDC', 'WY', 'WPM', 'WHR', 'WMB', 'WDAY', 'WYNN', 'YETI', 'ZEN', 'Z', 'ZIM', 'ZM', 'ZS']
local_tz = pytz.timezone('America/New_York')

file = open('stocksWithOnlyMonthlyOptions.txt',"r")
excludedTickers = file.read().split(',')
file.close()

def filterTickers(tickersList):
    filteredList = []

    with open("stocksWithOnlyMonthlyOptions.txt", "a") as excludedTickersFile:
        for ticker in tqdm(tickersList):
            if ticker in excludedTickers:
                continue
            
            data = callSchwabApi(ticker)
            if not data: # will trigger if bad request/status code 400
                excludedTickersFile.write(f',{ticker}')
                continue
            if not data['callExpDateMap']: # no friday options.  nearest friday options list is empty
                excludedTickersFile.write(f',{ticker}')
                continue
            elif checkIfEarningsSoon(ticker):
                continue
            else:
                # Add to filtered list
                filteredList.append(ticker)

    # Join the list items into a single string separated by commas
    list_as_string = ','.join(filteredList)

    # Open a file for writing and write the string
    with open('goodTickers.txt', 'w') as file:
        file.write(list_as_string)
    
    return filteredList

# Get nearest friday 
fromDate = datetime.datetime.now(local_tz).strftime("%Y-%m-%d")
toDate = datetime.datetime.now(local_tz)
toDate = toDate + datetime.timedelta( (4-toDate.weekday()) % 7 )
toDate = toDate.strftime("%Y-%m-%d")

access_token = ''     

@on_exception(expo, requests.exceptions.RequestException, max_time=60)
@sleep_and_retry
@limits(calls=120, period=60)
def callSchwabApi(ticker):
    url = f"https://api.schwabapi.com/marketdata/v1/chains?symbol={ticker}&strikeCount=1&fromDate={fromDate}&toDate={toDate}"
    #url = f"https://api.tdameritrade.com/v1/marketdata/chains?symbol={ticker}&strikeCount=1&fromDate=2022-01-01&toDate={toDate}"
    payload={}
    bearer = f"Bearer {access_token}"
    headers = {
        'Authorization': bearer
    }
    
    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.Timeout: # this is the timeout error from requests
        print("The Schab api request timed out, trying again")
        raise requests.RequestException # triggering this exception makes it try again with expo backoff
    except requests.HTTPError as err:
        status_code = err.response.status_code
        if status_code == 429: # rate limit error not caught by our set 120 limit
            raise requests.RequestException
        if status_code == 400: # bad request. probably bad ticker from ticker that is probably gone now.
            return
        if status_code == 401: # unauthorized.  Access token most likely refreshed in the middle of this script running
            set_access_token()
            raise requests.RequestException # triggering this exception makes it try again with expo backoff
    
    return data

# Check if earnings will be reported within the next two weeks
# Return True if yes
# Return False if no
@on_exception(expo, requests.exceptions.RequestException, max_time=60)
@sleep_and_retry
@limits(calls=60, period=60)
def checkIfEarningsSoon(symbol):
    today = datetime.datetime.now(local_tz)
    days_to_next_friday = (4 - today.weekday() + 7) % 7
    if days_to_next_friday == 0:
        days_to_next_friday = 7
    two_fridays_from_now = (today + datetime.timedelta(days=days_to_next_friday + 7)).strftime("%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")
    url = f"https://finnhub.io/api/v1/calendar/earnings?from={today}&to={two_fridays_from_now}&symbol={symbol}"

    headers = {
        'X-Finnhub-Token': 'ces2e5qad3i2r4r9nlvgces2e5qad3i2r4r9nm00'
    }

    try:
        response = requests.request("GET", url, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.HTTPError as e:
        raise requests.exceptions.RequestException
    except requests.Timeout:
        print("The finnhub api request timed out, trying again")
        raise requests.RequestException # triggering this exception makes it try again with expo backoff

    if result['earningsCalendar']:
        return True
    else:
        return False
    
def set_access_token():
    global access_token
    access_token = get_access_token()

try:
    set_access_token()
    access_token = 'I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.T4CCfP716dfAh6iufkm4JCbD4wvduNw7tzka1IbF1Xc@'
except:
    raise Exception("get access key error") 

filterTickers(symbolsList)
