import requests
import time
from concurrent.futures import ThreadPoolExecutor
from scripts_jserver import get_access_token

access_token = get_access_token()

# Define the URL and any necessary headers or payloads
url = "https://api.schwabapi.com/marketdata/v1/chains?symbol=MMM&strikeCount=1&fromDate=2024-06-01&toDate=2024-06-07"  # Replace with your actual endpoint
bearer = f"Bearer {access_token}"
headers = {
    'Authorization': bearer
}
payload = {}
count = 0

# Function to send a single request
def send_request():
    global count
    count += 1
    print(count, end=": ")
    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 429:
            print(response)
    except Exception as e:
        print(f"Request failed: {e}")

# Use ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    for _ in range(1300):
        executor.submit(send_request)
        # Slight delay between submissions to mimic rapid but not instant requests
        time.sleep(0.01)
