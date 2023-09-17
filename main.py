#!/usr/bin/python3
from finviz.screener import Screener
# from helper_funcs.folderFunctions import getCSVexportDirectory
from helper_funcs.filterFunctions import filterTickers
import pandas as pd
import os
import time

# # Filters
bigFilters = ["sh_curvol_o200", "sh_opt_option","sh_price_o100"] # Big filter
# tohFilters = ["sh_curvol_o2000", "sh_opt_option", "sh_price_20to100"] # 20-100 filter

# # Screening/scraping finviz process
big_list = Screener(filters=bigFilters, order="ticker")
# time.sleep(1)
# toh_list = Screener(filters=tohFilters, order="ticker")

# testFilter = ["sh_curvol_o20000", "sh_opt_option","sh_price_o100"]
# test_list = Screener(filters=testFilter,order="ticker")

print("")
print("Converting to lists...")
# Export CSV's
csvStream = big_list.to_csv()
df = pd.read_csv(csvStream, sep=",", header=None)
tickersList = df[df.columns[1]].values.tolist()[1:]

# Get and display current counts
print("before Count: " + str(len(tickersList)))

filtered_test_list = filterTickers(tickersList, "big_filtered")
print("after Count: " + str(len(filtered_test_list)))
