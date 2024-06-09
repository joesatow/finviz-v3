import os
import pytz
from datetime import datetime

def get_last_modified_time(file_path):
    # Replace 'your_file_path' with the path to the file you want to check
    file_path = file_path

    # Get the timestamp of when the file was last modified
    modification_time = os.path.getmtime(file_path)

    # Convert the timestamp to a more readable format
    utc_time = datetime.utcfromtimestamp(modification_time)

    # Convert UTC time to Eastern Standard Time (EST)
    eastern = pytz.timezone('US/Eastern')
    eastern_time = utc_time.replace(tzinfo=pytz.utc).astimezone(eastern)

    # Format the time in a 12-hour format with AM/PM
    readable_time = eastern_time.strftime('%Y-%m-%d %I:%M %p %Z')

    return readable_time

    #print("Last modified time in EST:", readable_time)

if __name__ == "__main__":
    print(get_last_modified_time("/home/jsat/github/finviz-v3/stocksWithOnlyMonthlyOptions.txt"))
