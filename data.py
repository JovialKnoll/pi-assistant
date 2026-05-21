import json
import logging
import urllib.request

import config


ATTEMPT_MAX = 3
logger = logging.getLogger(__name__)
logging.basicConfig(filename='data.log', encoding='utf-8', format='%(asctime)s %(message)s', level=logging.DEBUG)


def get_weather(lat, long):
    url = 'https://api.openweathermap.org/data/2.5/weather?appid={}&lat={}&lon={}'.format(
        config.KEY_OPENWEATHERMAP,
        lat,
        long,
    )
    for i in range(ATTEMPT_MAX):
        weather = get_weather_internal(url)
        if weather is not None:
            return weather
    logger.error(f'Failed to get weather {ATTEMPT_MAX} times')
    return None


def get_weather_internal(url):
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        logger.warning(f'Exception on urlopen: {e}')
        return None
    code = response.getcode()
    if code != 200:
        logger.warning(f'Response code was {code}')
        return None
    content = response.read()
    weather = json.loads(content)
    if weather['cod'] == '404':
        logger.warning('Weather returned 404')
        return None
    #with open('test.json', 'w') as f:
    #    json.dump(weather, f, indent=4)
    return weather
