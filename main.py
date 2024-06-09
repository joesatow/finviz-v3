#!/usr/bin/python3
from helper_funcs.folderFunctions import runFolderChecks
from helper_funcs.filterFunctions import filterTickers
from helper_funcs.webpageFunctions import generateWebPage
from finviz.screener import Screener
import pandas as pd
import time

# Wipe chart folders, re-create new ones, set current directory
runFolderChecks()

# Filters
bigFilters = ["sh_curvol_o200", "sh_opt_option","sh_price_o100"] # Big filter
tohFilters = ["sh_curvol_o2000", "sh_opt_option", "sh_price_20to100"] # 20-100 filter

# Screening/scraping finviz process
bigScreener = Screener(filters=bigFilters, order="ticker")
time.sleep(1)
tohScreener = Screener(filters=tohFilters, order="ticker")

print("")
print("Converting to lists...")
# Export CSV's
csvStream = bigScreener.to_csv()
df = pd.read_csv(csvStream, sep=",", header=None)
bigScreener_TickersList = df[df.columns[1]].values.tolist()[1:] # taking first column of dataframe is the tickers column.  cutting off first elemnt will remove unnecessary header.

csvStream = tohScreener.to_csv()
df = pd.read_csv(csvStream, sep=",", header=None)
tohScreener_TickersList = df[df.columns[1]].values.tolist()[1:] # taking first column of dataframe is the tickers column.  cutting off first elemnt will remove unnecessary header.

# Get and display current counts
big_count = str(len(bigScreener_TickersList))
toh_count = str(len(tohScreener_TickersList))
print("Big count: " + big_count)
print("20-100 count: " + toh_count)
print()

# Filter tickers
filtered_big_list = filterTickers(bigScreener_TickersList, "big_filtered")
filtered_toh_list = filterTickers(tohScreener_TickersList, "toh_filtered")
print()

# Display filtered counts
filtered_big_count = str(len(filtered_big_list))
filtered_toh_count = str(len(filtered_toh_list))
print("Filtered big count: " + filtered_big_count)
print("Filtered 20-100 count: " + filtered_toh_count)
print()

# Change data on screener object to filtered ticker lists
bigScreener.data = filtered_big_list
tohScreener.data = filtered_toh_list

# Get charts
bigScreener.get_charts(period='d') # daily
bigScreener.get_charts(period='w') # weekly
tohScreener.get_charts(period='d') # daily
tohScreener.get_charts(period='w') # daily

# Generate web page
generateWebPage(
    filtered_big_list, 
    filtered_toh_list,
    [
        big_count,
        toh_count,
        filtered_big_count,
        filtered_toh_count
    ]
)