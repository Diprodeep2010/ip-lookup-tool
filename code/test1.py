from urllib import urlopen
from contextlib import closing
import json

# Automatically geolocate the connecting IP
url = 'http://freegeoip.net/json/'

response=urlopen(url)
print response.read();
location = json.loads(response.read())
print(location)
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']
location_zip = location['zipcode']


