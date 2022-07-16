import datetime
from pytz import timezone
from typing import Union

import requests

from telegram_weather.settings import OPENWEATHER_APIKEY

from .models import Users


class WeatherService:
    _CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
    _DAYS_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'
    _WEATHER_ICON_URL = 'https://openweathermap.org/img/wn/{}@2x.png'
    _APIKEY = OPENWEATHER_APIKEY

    def __init__(self, user_id: Union[int, str]):
        self.user_id = user_id
        self.user = Users.objects.get(uid=user_id)
        location = self.user.location.split(',')
        self.location = {'lat': location[0], 'lon': location[1], 'city_name': self.user.city_name}

    def get_current_weather(self) -> dict:
        data = requests.get(self._CURRENT_WEATHER_URL, params={'lat': self.location['lat'],
                                                               'lon': self.location['lon'],
                                                               'appid': self._APIKEY, 'lang': 'ru',
                                                               'units': 'metric'}).json()
        desc = data['weather'][0]['description']
        cur_temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        output = {
            'description': desc,
            'temp': cur_temp,
            'feels': feels_like,
            'city': self.location['city_name'],
            'icon': self._WEATHER_ICON_URL.format(data['weather'][0]['icon'])
        }
        return output

    def get_today_weather(self) -> dict:
        data = requests.get(self._DAYS_WEATHER_URL, params={'lat': self.location['lat'],
                                                               'lon': self.location['lon'],
                                                               'appid': self._APIKEY, 'lang': 'ru',
                                                               'units': 'metric'}).json()
        result = {'weather': [], 'city_name': self.location['city_name']}
        for hour in data['list']:
            date = datetime.datetime.fromtimestamp(hour['dt'], tz=timezone('Europe/Moscow'))
            json_output = {
                'date': date.strftime("%H:%M"),
                'temp': hour['main']['temp'],
                'icon': self._WEATHER_ICON_URL.format(hour['weather'][0]['icon']),
                'description': hour['weather'][0]['description']
            }
            result['weather'].append(json_output)
            if len(result['weather']) >= 12:
                break
        return result

    def get_days_weather(self) -> dict:
        data = requests.get(self._DAYS_WEATHER_URL, params={'lat': self.location['lat'],
                                                            'lon': self.location['lon'],
                                                            'appid': self._APIKEY, 'lang': 'ru',
                                                            'units': 'metric'}).json()
        result = {'weather': [], 'city_name': self.location['city_name']}
        day_temp = []
        cur_day = 0
        icon = None
        for hour in data['list']:
            date = datetime.datetime.fromtimestamp(hour['dt'], tz=timezone('Europe/Moscow'))
            if not icon:
                icon = self._WEATHER_ICON_URL.format(hour['weather'][0]['icon'])
            if cur_day != date.day:
                if cur_day != 0:
                    result['weather'].append({'date': date.strftime('%A, %d.%m'),
                                     'temp': round(sum(day_temp) / len(day_temp), 2),
                                     'icon': icon})
                cur_day = date.day
                icon = None
            day_temp.append(hour['main']['temp'])
        return result
