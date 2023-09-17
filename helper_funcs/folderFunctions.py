import os

# Change directory to path of main directory of this software
mainDirectoy = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
os.chdir(mainDirectoy)

# Create csv exports file if it doesn't exist
if not os.path.exists("csvExports"):
    os.makedirs("csvExports")
