import requests
from bs4 import BeautifulSoup

import weather_scripts as weather


# note to run server cd to weather folder and use the command 'python manage.py runserver'


def test():
	url = weather.get_wg_url()
	key, values = weather.get_current_conditions(url)
	print(key)
	print(values)

######################################################
#		Break!  Do Not Edit Below! For records!		 #
######################################################


# Current test. Archive below when starting a new test
# Note this test will not work in Sublime Text, use command prompt
def test2():
	loc = weather.get_loc()
	coord = weather.str_to_coord(loc)
	print(coord)
	


# test for getting a forecast and printing it out
def test1():
	url = weather.get_wgapi_url()
	forecast = weather.get_forecast(url)
	weather.print_forcast(forecast)


######################################################
#		Break!  Do Not Edit Above! For records!		 #
######################################################


if __name__ == '__main__':
	test()