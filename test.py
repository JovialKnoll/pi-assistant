#!/usr/bin/env python3

import sys

import renderer


image = renderer.get_page(0)
image.save("test.png")
sys.exit()
