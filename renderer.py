from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import config
import data


# drawing vars
small_font = ImageFont.truetype(
    Path(__file__).parent / "fonts" / "dejavu" / "DejaVuSans-Bold.ttf",
    16)
medium_font = ImageFont.truetype(
    Path(__file__).parent / "fonts" / "dejavu" / "DejaVuSans.ttf",
    20)
large_font = ImageFont.truetype(
    Path(__file__).parent / "fonts" / "dejavu" / "DejaVuSans-Bold.ttf",
    24)
icon_font = ImageFont.truetype(
    Path(__file__).parent / "fonts" / "meteocons.ttf",
    48)
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MARGIN_X = 0
MARGIN_Y = 1
SPACING = 1


def _get_celsius(kelvin):
    return kelvin - 273.15


def _get_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def _get_size(bbox):
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


_width_for_temp_c = _get_size(large_font.getbbox("000°C"))[0]
_width_for_temp_both = _get_size(large_font.getbbox("100°F000°C"))[0]


# bbox = left, upper, right, and lower pixel
def _display_weather(label, weather):
    image = Image.new("RGB", (config.WIDTH, config.HEIGHT), color=WHITE)
    draw = ImageDraw.Draw(image)

    label_bbox = medium_font.getbbox(label)
    label_y_offset = label_bbox[1]
    label_bottom = label_bbox[3] - label_y_offset
    draw.text(
        (MARGIN_X, MARGIN_Y - label_y_offset),
        label, font=medium_font, fill=BLACK)
    print("label_bottom: " + str(label_bottom))

    description = weather["weather"][0]["description"]
    description = description[0].upper() + description[1:]
    description_bbox = small_font.getbbox(description)
    description_y_offset = description_bbox[1]
    description_height = description_bbox[3] - description_y_offset
    description_top = config.HEIGHT - MARGIN_Y - description_height
    draw.text(
        (MARGIN_X, description_top - description_y_offset),
        description, font=small_font, fill=BLACK)
    print("description_top: " + str(description_top))

    main = weather["weather"][0]["main"]
    main_bbox = large_font.getbbox(main)
    main_y_offset = main_bbox[1]
    main_height = main_bbox[3] - main_y_offset
    main_top = description_top - SPACING - main_height
    draw.text(
        (MARGIN_X, main_top - main_y_offset),
        main, font=large_font, fill=BLACK)
    print("main_top: " + str(main_top))

    icon = ICON_MAP[weather["weather"][0]["icon"]]
    icon_bbox = icon_font.getbbox(icon)
    icon_y_offset = icon_bbox[1]
    icon_height = icon_bbox[3] - icon_y_offset
    icon_top = main_top - SPACING - icon_height
    draw.text(
        (MARGIN_X, icon_top - icon_y_offset),
        icon, font=icon_font, fill=BLACK)

    temp_c = _get_celsius(weather["main"]["temp"])
    temp_f = _get_fahrenheit(temp_c)
    feels_like_c = _get_celsius(weather["main"]["feels_like"])
    feels_like_f = _get_fahrenheit(feels_like_c)

    temperature_c = "%d°C" % round(temp_c)
    (font_width, font_height) = _get_size(large_font.getbbox(temperature_c))
    xy = (config.WIDTH - font_width, 0)
    draw.text(xy, temperature_c, font=large_font, fill=BLACK)
    old_font_height = font_height
    temperature_f = "%d°F" % round(temp_f)
    (font_width, font_height) = _get_size(large_font.getbbox(temperature_f))
    xy = (config.WIDTH - font_width - _width_for_temp_c, 0)
    draw.text(xy, temperature_f, font=large_font, fill=BLACK)
    old_font_height = max(old_font_height, font_height)

    y = xy[1] + old_font_height
    temperature_c = "%d°C" % round(feels_like_c)
    (font_width, font_height) = _get_size(large_font.getbbox(temperature_c))
    xy = (config.WIDTH - font_width, y)
    old_font_height = font_height
    draw.text(xy, temperature_c, font=large_font, fill=BLACK)
    temperature_f = "%d°F" % round(feels_like_f)
    (font_width, font_height) = _get_size(large_font.getbbox(temperature_f))
    xy = (config.WIDTH - font_width - _width_for_temp_c, y)
    draw.text(xy, temperature_f, font=large_font, fill=BLACK)
    old_font_y = xy[1] + max(old_font_height, font_height)

    (font_width, font_height) = _get_size(small_font.getbbox("feels"))
    xy = (config.WIDTH - font_width - _width_for_temp_both, y)
    draw.text(xy, "feels", font=small_font, fill=BLACK)
    feels_font_height = font_height

    (font_width, font_height) = _get_size(small_font.getbbox("like"))
    xy = (config.WIDTH - font_width - _width_for_temp_both, y + feels_font_height)
    draw.text(xy, "like", font=small_font, fill=BLACK)

    humidity = "%d%%" % weather["main"]["humidity"]
    (font_width, font_height) = _get_size(large_font.getbbox(humidity))
    xy = (config.WIDTH - font_width, old_font_y)
    draw.text(xy, humidity, font=large_font, fill=BLACK)
    old_font_y = xy[1] + font_height

    windspeed = "%dm/s" % weather["wind"]["speed"]
    (font_width, font_height) = _get_size(large_font.getbbox(windspeed))
    xy = (config.WIDTH - font_width, old_font_y)
    draw.text(xy, windspeed, font=large_font, fill=BLACK)
    old_font_y = xy[1] + font_height

    winddeg = weather["wind"]["deg"]
    midway = (config.HEIGHT - old_font_y) // 2
    lx = config.WIDTH - midway
    ly = config.HEIGHT - midway
    #print(old_font_y)
    #print(config.HEIGHT)
    #print((lx, ly))
    draw.circle((lx, ly), 14, outline=BLACK)
    draw.line(((lx, ly), (lx, ly - 14)), fill=BLACK)

    return image


def get_page(page_index):
    page_config = config.CONFIG_PAGES[page_index]
    weather = data.get_weather(page_config['lat'], page_config['long'])
    if not weather:
        return None
    return _display_weather(page_config['label'], weather)
