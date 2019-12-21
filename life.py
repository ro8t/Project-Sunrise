# Dependencies
import requests
import json
import pprint
import pandas as pd

# API Keys
from config import yelp

# DB
from sqlalchemy import create_engine

api_key = yelp
headers = {'Authorization': 'Bearer %s' % api_key}

url='https://api.yelp.com/v3/businesses/search'
 
# In the dictionary, term can take values like food, cafes or businesses like McDonalds
params = {'term':'climbing','location':'San Francisco'}
# Making a get request to the API
req = requests.get(url, params=params, headers=headers)

# proceed only if the status code is 200
# print('The status code is {}'.format(req.status_code))

# printing the text from the response 
response_json = req.json()
# pprint(response_json)

bup = response_json['businesses']
name = []
lat = []
lon = []
rating = []
for business in bup:
    name.append(business['name'])
    lat.append(business['coordinates']['latitude'])
    lon.append(business['coordinates']['longitude'])
    rating.append(business['rating'])
#print(name)
#print(lat)
yelp_df = pd.DataFrame(
    {'Name': name,
     'Rating': rating,
     'Latitude': lat,
     'Longitude': lon})


