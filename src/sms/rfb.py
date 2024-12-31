import requests
from sms_api_key import get_rfb_path

# api-endpoint
URL = get_rfb_path()
  
# location given here
#location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
#PARAMS = {'address':location}
  
# sending get request and saving the response as response object
r = requests.get(url = URL)

