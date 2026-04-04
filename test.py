#!/usr/bin/env python3

from pathlib import Path
import json
import sys
from datetime import date

#import config
#import data
import renderer


#page_config = config.CONFIG_PAGES[0]
#weather = data.get_weather(page_config['lat'], page_config['long'])
with open(Path(__file__).parent / 'test.json', 'r') as f:
    weather = json.load(f)
image = renderer.get_weather_display("Test", date(2026, 12, 20), weather)
image.save(Path(__file__).parent / 'test.png')
sys.exit()
