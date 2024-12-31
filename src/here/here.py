
from here.here_api_key import get_API_KEY

# Replace with your HERE API key
import requests
import time
API_KEY = get_API_KEY()

def get_ride_time(lat1, long1, lat2, long2):

    time.sleep(1) #for rate limiting
    ORIGIN = str(lat1) + "," + str(long1)
    DEST = str(lat2) + "," + str(long2)

    url = "https://router.hereapi.com/v8/routes?"
    params = {
    "transportMode": "car",
    "origin": ORIGIN,
    "destination": DEST,
    "return": "summary",
    "apiKey": get_API_KEY()
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Check if response was successful
    if response.status_code == 200:
    # Parse JSON response
        route_data = response.json()
        print(route_data)

        # Extract duration
        try:
            duration = route_data['routes'][0]['sections'][0]['summary']['duration']
        except:
            duration = 10000


        print(f"Duration: {duration} seconds")

        # Convert duration to minutes and seconds
        minutes = duration // 60
        seconds = duration % 60
        print(f"Duration: {minutes} minutes {seconds} seconds")

        return duration
    else:
        print("Error :( :", response.status_code)
        print(f"Error {response.status_code}: {response.reason}")
        print("Response Content:")
        print(response.text)
