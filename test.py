#!/usr/bin/env python3

import sys

import config
import data
import renderer


page_config = config.CONFIG_PAGES[0]
weather = data.get_weather(page_config['lat'], page_config['long'])
image = renderer.get_weather_display(page_config['label'], weather)
image.save("test.png")
sys.exit()
