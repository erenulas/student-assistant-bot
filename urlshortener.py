import requests
import json

#   This is the API KEY for google url shortener service
API_KEY = <API_KEY>

def shorten(long_url):
    # creation of the base url
    url = "https://www.googleapis.com/urlshortener/v1/url?key=" + API_KEY    
    data = json.dumps({'longUrl': long_url})  
    # sends the long url with other parameters to get the shortened version of it                                              
    result = requests.post(url, headers={'content-type': 'application/json'}, data=data)    
    temp = result.json()
    short_url = temp['id']
    return short_url
