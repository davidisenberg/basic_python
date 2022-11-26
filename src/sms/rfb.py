import requests
  
# api-endpoint
URL = "http://davidisenberg.pythonanywhere.com/send?user=nothingbutnet&message=Daily RFB"
  
# location given here
#location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
#PARAMS = {'address':location}
  
# sending get request and saving the response as response object
r = requests.get(url = URL)

