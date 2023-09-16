#!/usr/bin/python3
from finviz.screener import Screener
import time

# Filters
bigFilters = ["sh_curvol_o200", "sh_opt_option","sh_price_o100"] # Big filter
tohFilters = ["sh_curvol_o2000", "sh_opt_option", "sh_price_20to100"] # 20-100 filter

# Screening/scraping finviz process
big_list = Screener(filters=bigFilters, order="ticker")
time.sleep(1)
toh_list = Screener(filters=tohFilters, order="ticker")

print("test")