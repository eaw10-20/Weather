from bs4 import BeautifulSoup
import requests
import re


def main():
	url = 'https://forecast.weather.gov/MapClick.php?lat=33.6745&lon=-117.2274&unit=0&lg=english&FcstType=text&TextType=1'

	forecast = get_forecast(url)
	# get temp forecast
	temps = get_temps(forecast)
	# print out temperatures gotten
	print_temps(temps)


# gets the forecast from an input url
def get_forecast(url):
	# get html text from url
	source = requests.get(url).text
	# convert html to format that can be printed
	soup = BeautifulSoup(source, 'lxml')
	# print soup (prettify adds indents)
	# print(soup.prettify())

	# allocate array for table
	tables = []

	# put all tables taken from the page into a list
	for table in soup.find_all('table'):
		#stuff
		tables += table

	# the third table has the forecast. This may possibly change causing an error in the future
	forecast = tables[3].text
	return forecast


# note this function doesn't deal with day and night in one line
# if this is a possibility consider revising
def is_night(forecast, start, end):
	if 'low' in forecast[start:end]:
		return True
	return False


# returns an array of temps from a text forecast
def get_temps(forecast):
	temps = [['-' for x in range(7)] for y in range(7)]		# 2d array which holds temps for day and night
	filled = [[False for x in range(7)] for y in range(7)]	# to mark when spot is filled
	cont = True		# false if no more temps
	day = 0			# determines which day it is for forecast input

	#get range within which to look
	end = 0
	while cont == True:
		# determine range of text whithin which to search
		start = forecast.find(':', end)
		end = forecast.find('\n', start)

		#determine whether it is night within this forecast section and note for array
		night = is_night(forecast, start, end)
		a = 1 if night else 0

		#increment day if necessary
		if filled[a][day] == True:
			day += 1

		# get temperature
		temps[a][day] = re.search(r'\d+', forecast[start:end]).group()
		filled[a][day] = True

		#keep going?
		if ':' not in forecast[end:]:
			cont = False

	return temps

def print_temps(temps):
	for i in range(len(temps)):
		print(str(temps[0][i]) + '   ' + str(temps[1][i]))


if __name__ == '__main__':
	main()