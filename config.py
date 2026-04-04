from pathlib import Path
import json

_CONFIG_FILE = Path(__file__).parent / 'config.json'
_config = None
with open(_CONFIG_FILE) as file:
    _config = json.load(file)

KEY_OPENWEATHERMAP = _config['key_openweathermap']
CONFIG_PAGES = _config['config_pages']

WIDTH = 250
HEIGHT = 122
DELAY = 900
CRON_EXPRESSION = '*/15 * * * *'
