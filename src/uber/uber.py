from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber.uber_api_key import get_client_id, get_client_secret

import requests

# files = {
#     'client_id': (None, open('CLIENT_ID>', 'rb')),
#     'client_secret': (None, open('CLIENT_SECRET>', 'rb')),
#     'grant_type': (None, 'client_credentials'),

#           -F 'grant_type=client_credentials'\
#       -F 'scope="SPACE_DELIMITED_LIST_OF_SCOPES"\
# }
# response = requests.post('https://login.uber.com/oauth/v2/token', files=files)



# session = Session(server_token=<TOKEN>)
# client = UberRidesClient(session)

# #def get_ride_estimate(start_lat, start_long, end_lat, end_long)

# response = client.get_price_estimates(
#     start_latitude=37.770,
#     start_longitude=-122.411,
#     end_latitude=37.791,
#     end_longitude=-122.405,
#     seat_count=2
# )

#https://developer.uber.com/docs/guest-rides/guides/authentication
# estimate = response.json.get('prices')

CLIENT_ID = get_client_id
CLIENT_SECRET = get_client_secret()

# Set API endpoint and payload
url = "https://auth.uber.com/oauth/v2/token"
payload = {
"client_secret": get_client_secret(),
"client_id": get_client_id(),
"grant_type": "client_credentials",
"scope": "history"
}

# Set headers (Content-Type: application/x-www-form-urlencoded)
headers = {"Content-Type": "application/x-www-form-urlencoded"}

# Send POST request
response = requests.post(url, data=payload, headers=headers)

# Check if response was successful
if response.status_code == 200:
# Parse JSON response
    token_response = response.json()
    access_token = token_response["access_token"]
    print("Access Token:", access_token)
else:
    print("Error :( :", response.status_code)
    print(f"Error {response.status_code}: {response.reason}")
    print("Response Content:")
    print(response.text)


