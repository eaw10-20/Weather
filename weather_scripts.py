from bs4 import BeautifulSoup
import requests, re
from geopy.geocoders import Nominatim


defalt_lat = str(33.6745)
defalt_lon = str(-117.2274)

def main():
	url = get_wgapi_url()

	forecast = get_forecast(url)
	print(forecast)


# get weather.gov api url
def get_wgapi_url():
	# input coordinates converted to string format for url
	lat = defalt_lat
	lon = defalt_lon
	# request url based on input latitude and longitude
	return 'https://api.weather.gov/points/'+lat+','+lon


# get weather.gov link for web scraping
def get_wg_url():
	# input coordinates converted to string format for url
	lat = defalt_lat
	lon = defalt_lon
	# request url based on input latitude and longitude
	return 'https://forecast.weather.gov/MapClick.php?lat='+lat+'&lon='+lon



def get_loc():
	# input string
	loc = input("Enter a city: ")
	return str_to_coord(loc)


def str_to_coord(loc):
	# converts an input string into a set of coordinates
	# https://geopy.readthedocs.io/en/latest/#nominatim
	geolocator = Nominatim(user_agent="personal weather app")
	# attempt to find a coordinate for given string. Exception for bad input (hopefully)
	query = geolocator.geocode(loc)
	try:
		lat = query.latitude
		lon = query.longitude
	except:
		print("Location unavailable")
		return [0, 0]
	return [lat, lon]


# gets the forecast from an input url
def get_forecast(url):
	# note that this should be edited to remove request redundancies
	r = requests.get(url)
	properties = r.json()['properties']

	# example of output of properties
	 # {'@id': 'https://api.weather.gov/points/33.6745,-117.2274',
	 # '@type': 'wx:Point',
	 # 'cwa': 'SGX',
	 # 'forecastOffice': 'https://api.weather.gov/offices/SGX',
	 # 'gridId': 'SGX',
	 # 'gridX': 60,
	 # 'gridY': 55,
	 # 'forecast': 'https://api.weather.gov/gridpoints/SGX/60,55/forecast',
	 # 'forecastHourly': 'https://api.weather.gov/gridpoints/SGX/60,55/forecast/hourly',
	 # 'forecastGridData': 'https://api.weather.gov/gridpoints/SGX/60,55',
	 # 'observationStations': 'https://api.weather.gov/gridpoints/SGX/60,55/stations',
	 # 'relativeLocation': {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-117.263547, 33.688302]}, 'properties': {'city': 'Canyon Lake', 'state': 'CA', 'distance': {'value': 3679.9537458897, 'unitCode': 'unit:m'}, 'bearing': {'value': 114, 'unitCode': 'unit:degrees_true'}}},
	 # 'forecastZone': 'https://api.weather.gov/zones/forecast/CAZ048',
	 # 'county': 'https://api.weather.gov/zones/county/CAC065',
	 # 'fireWeatherZone': 'https://api.weather.gov/zones/fire/CAZ248',
	 # 'timeZone': 'America/Los_Angeles',
	 # 'radarStation': 'KSOX'}

	# get forecast information for specific url
	url = properties['forecast']
	r = requests.get(url)
	pointInfo = r.json()['properties']

	# pointInfo variables:
	 # 'updated' - time and date forecast was updated
	 # 'generatedAt' - time and date request was sent
	 # 'elevation' - gives dictionary with 'value' and 'unitCode'
	 # 'periods' - dictionary containing the forecast info

	forecast = pointInfo['periods']

	#forecast is a list of dictionaries. An example of the first value of list:
	 # {"number": 1,
	 # "name": "This Afternoon",
	 # "startTime": "2020-07-09T17:00:00-07:00",
	 # "endTime": "2020-07-09T18:00:00-07:00",
	 # "isDaytime": true,
	 # "temperature": 94,
	 # "temperatureUnit": "F",
	 # "temperatureTrend": null,
	 # "windSpeed": "15 mph",
	 # "windDirection": "S",
	 # "icon": "https://api.weather.gov/icons/land/day/skc?size=medium",
	 # "shortForecast": "Sunny",
	 # "detailedForecast": "Sunny, with a high near 94. South wind around 15 mph, with gusts as high as 25 mph."
	 # },{...},...

	return forecast


# TODO
def get_current_conditions(url):
	# get html from link using requests
	source = requests.get(url).text
	# parse info from html
	soup = BeautifulSoup(source, 'html5lib')
	# contaions all current conditions at given location in html
	current_conditions = soup.find('div', id='current-conditions')


	# get and sort out current conditions to return
	key, values = [],[]
	key.append('Location')
	values.append(current_conditions.find('h2', class_='panel-title').text)
	# TODO: elevation

	# pull from current conditions summary and add them to list
	summary = current_conditions.find('div', id='current_conditions-summary')
	for entry in summary.find_all('p'):
		values.append(entry.text)
	key += ['Sky', 'F', 'C']

	# pull from current conditions detail and add them to list
	detail = current_conditions.find('div', id='current_conditions_detail')
	for entry in detail.find_all('td'):
		if entry.find_all('b'):
			key.append(entry.b.text)
		else:
			values.append(entry.text)
	return [key, values]



def print_forcast(forecast):
	for i in forecast:
		print(i['name'] + " will be " + i['shortForecast'] + " and " + str(i['temperature']) + i['temperatureUnit'] + ".")



if __name__ == '__main__':
	main()