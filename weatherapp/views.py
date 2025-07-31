from django.shortcuts import render
from django.contrib import messages
import requests
from datetime import datetime
from collections import OrderedDict
from django.conf import settings

def weather(request):
    context = {}  
    if request.method == "POST":
        city = request.POST.get('city')

        if city:
            apikey = settings.WEATHER_API_KEY
            weather_url = f"{settings.WEATHER_URL}?q={city}&appid={apikey}&units=metric"
            forecast_url = f"{settings.FORECAST_URL}?q={city}&appid={apikey}&units=metric"
            try:
                response = requests.get(weather_url, timeout=5)
                data = response.json()

                if data.get("cod") == 200:
                    description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    city = data['name']
                    country = data['sys']['country']
                    icon_code = data['weather'][0]['icon']
                    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    humidity = data['main']['humidity']
                    wind = data['wind']['speed']
                    weather_condition = data['weather'][0]['main']

                    context.update({
                        'description': description,
                        'temperature': temperature,
                        'city': city,
                        'country':country,
                        'icon_url': icon_url,
                        'humidity': humidity,
                        'wind': wind,
                        'weather_condition':weather_condition
                    })
                    
                    try:
                        forecast_response = requests.get(forecast_url, timeout=5)
                        forecast_data = forecast_response.json()

                        if forecast_data.get("cod") == "200":
                            daily_forecast = OrderedDict()

                            for item in forecast_data["list"]:
                                date_time = item['dt_txt']
                                if "12:00:00" in date_time:
                                    day_name = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").strftime('%A')
                                    temp = item['main']['temp']
                                    desc = item['weather'][0]['description']
                                    iconcode = item['weather'][0]['icon']
                                    iconurl = f"http://openweathermap.org/img/wn/{iconcode}@2x.png"

                                    daily_forecast[day_name]={
                                        'date_time' : day_name,
                                        'temp' : temp,
                                        'desc' : desc,
                                        'iconurl' : iconurl
                                    }

                                    if len(daily_forecast) == 5:
                                        break

                            forecast_list = list(daily_forecast.values())    
                            context["forecast"] = forecast_list

                        else:
                            messages.error(request,"Forecast data not available")

                    except requests.exceptions.RequestException:
                        messages.error(request, "Error getting forecast data.")
                else:
                    messages.error(request, "Please enter a valid city name")

            except requests.exceptions.RequestException:
                messages.error(request, "Network error. Please try again.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    return render(request, 'weather.html', context)
