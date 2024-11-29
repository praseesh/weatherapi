from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from decouple import config
from datetime import datetime

def index(request):
    cities = City.objects.all()
    api_key = config('API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()  
    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city.name, api_key)).json()
        weather = {
            'city': city.name,
            'temperature': round(city_weather['main']['temp'] - 273.15, 2),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'country': city_weather['sys']['country'],
            'sunrise': datetime.utcfromtimestamp(city_weather['sys']['sunrise']).strftime('%H:%M:%S'),
            'sunset': datetime.utcfromtimestamp(city_weather['sys']['sunset']).strftime('%H:%M:%S'),
            'windspeed': city_weather['wind']['speed'],
        }
        
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)






