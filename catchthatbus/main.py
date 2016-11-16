import requests
import sys
import dateutil.parser
import datetime
import time


stopPointId = '490004539E'
app_id = 'xxx'
app_key= 'xxxxxx'

payload = {'stopPointId': stopPointId, 'app_id': app_id, 'app_key': app_key}

try:
    r = requests.get('https://api.tfl.gov.uk/Line/c10/Arrivals', params=payload)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

json = r.json()
now = datetime.datetime.now()

for bus_data in json:
    expectedArrival = bus_data['expectedArrival']
    date = dateutil.parser.parse(expectedArrival)

    # convert to unix timestamp
    d1_ts = time.mktime(now.timetuple())
    d2_ts = time.mktime(date.timetuple())

    # they are now in seconds, subtract and then divide by 60 to get minutes.
    expected_bus_in = (d2_ts - d1_ts) / 60
    print('Expected Bus in {} minutes'.format(int(round(expected_bus_in, 0))))


