import os
import shutil

# Change directory to path of main directory of this software
mainDirectoy = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
os.chdir(mainDirectoy)

# Wipe charts folder if it does exist
if os.path.exists("webpage/charts"):
    shutil.rmtree("webpage/charts")

# Create charts folders they don't exist
if not os.path.exists("webpage/charts"):
    os.makedirs("webpage/charts")

if not os.path.exists("webpage/charts/big-daily"):
    os.makedirs("webpage/charts/big-daily")

if not os.path.exists("webpage/charts/big-weekly"):
    os.makedirs("webpage/charts/big-weekly")

if not os.path.exists("webpage/charts/toh-daily"):
    os.makedirs("webpage/charts/toh-daily")

if not os.path.exists("webpage/charts/toh-weekly"):
    os.makedirs("webpage/charts/toh-weekly")

def getCSVexportDirectory():
    pass