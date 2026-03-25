#!/usr/bin/env python3

import sys
import time
import busio
import board
import digitalio
import threading

from adafruit_debouncer import Debouncer
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from PIL import ImageChops

import config
import renderer


# display
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
display = Adafruit_SSD1680(config.HEIGHT, config.WIDTH, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)
display.rotation = 1

# input
up_button = digitalio.DigitalInOut(board.D6)
up_button.switch_to_input()
up_switch = Debouncer(up_button)
down_button = digitalio.DigitalInOut(board.D5)
down_button.switch_to_input()
down_switch = Debouncer(down_button)

page_count = len(config.CONFIG_PAGES)


class ImageThread(threading.Thread):
    def __init__(self, images, refreshes, thread_id):
        super(ImageThread, self).__init__(daemon=True)
        self.images = images
        self.refreshes = refreshes
        self.thread_id = thread_id

    def run(self):
        while True:
            current_image = self.images[self.thread_id]
            new_image = renderer.get_page(self.thread_id)
            if not current_image \
            or (new_image and ImageChops.difference(current_image, new_image).getbbox()):
                self.images[self.thread_id] = new_image
                self.refreshes[self.thread_id] = True
            time.sleep(config.DELAY)


def main():
    images = [None] * page_count
    refreshes = [False] * page_count
    threads = [
        ImageThread(images, refreshes, i)
        for i in range(page_count)
    ]
    for thread in threads:
        thread.start()
    page_index = 0

    while True:
        up_switch.update()
        down_switch.update()
        if up_switch.fell:
            page_index -= 1
            page_index %= page_count
            refreshes[page_index] = True
        if down_switch.fell:
            page_index += 1
            page_index %= page_count
            refreshes[page_index] = True
        if refreshes[page_index] and images[page_index]:
            display.image(images[page_index])
            display.display()
            refreshes[page_index] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
sys.exit()
