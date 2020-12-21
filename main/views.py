from django.shortcuts import render
import weather_scripts as ws

# used the nws api to get forecast information in weather_scripts.py
# forecast info is returned in json format
url = ws.get_wgapi_url()
forecast = ws.get_forecast(url)

# current conditions are pulled off of weather.gov page
# list of current conditions returned in list of keys and corresponding values
url = ws.get_wg_url()
conditions_key, conditions_val = ws.get_current_conditions(url)

# Create your views here.
def home(request):
	context = {
	'forecast': forecast,
	'c_key': conditions_key,
	'c_val': conditions_val,
	}
	return render(request, 'main/home.html', context)