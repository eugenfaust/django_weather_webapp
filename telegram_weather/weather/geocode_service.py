import requests
from telegram_weather.settings import DEBUG


def get_location_by_ip(ip: str) -> [str, str]:
    if DEBUG:
        api_url = 'http://ipinfo.io/json'
    else:
        api_url = 'http://ipinfo.io/{}/json'.format(ip)
    result = requests.get(api_url)
    if result.status_code == 200:
        location = result.json()
        if location:
            return location['loc'].split(',')
    return None
