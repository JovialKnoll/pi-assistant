#!/usr/bin/env python3

import sys

import config
import data


page_config = config.CONFIG_PAGES[0]
weather = data.get_weather(page_config['lat'], page_config['long'])
print(weather)
sys.exit()
