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


full_temp_c_width = large_font.getbbox("000°C")[2]
full_temp_both_width = large_font.getbbox("100°F000°C")[2]


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

    temp_c_num = _get_celsius(weather["main"]["temp"])
    temp_c = "%d°C" % round(temp_c_num)
    temp_c_bbox = large_font.getbbox(temp_c)
    temp_c_y_offset = temp_c_bbox[1]
    temp_c_width = temp_c_bbox[2]
    temp_c_bottom = temp_c_bbox[3] - temp_c_y_offset
    draw.text(
        (config.WIDTH - temp_c_width, MARGIN_Y - temp_c_y_offset),
        temp_c, font=large_font, fill=BLACK)
    print("temp_c_bottom: " + str(temp_c_bottom))

    temp_f_num = _get_fahrenheit(temp_c_num)
    temp_f = "%d°F" % round(temp_f_num)
    temp_f_bbox = large_font.getbbox(temp_f)
    temp_f_y_offset = temp_f_bbox[1]
    temp_f_width = temp_f_bbox[2]
    temp_f_bottom = temp_f_bbox[3] - temp_f_y_offset
    draw.text(
        (config.WIDTH - full_temp_c_width - temp_f_width, MARGIN_Y - temp_f_y_offset),
        temp_f, font=large_font, fill=BLACK)
    print("temp_f_bottom: " + str(temp_f_bottom))
    """
    feels_like_c_num = _get_celsius(weather["main"]["feels_like"])
    feels_like_c = "%d°C" % round(feels_like_c_num)
    feels_like_c_bbox = large_font.getbbox(feels_like_c)
    feels_like_c_y_offset = feels_like_c_bbox[1]
    feels_like_c_width = feels_like_c_bbox[2]
    feels_like_c_bottom = MARGIN_Y + temp_c_bottom + SPACING + feels_like_c_bbox[3] - feels_like_c_y_offset
    draw.text(
        (config.WIDTH - feels_like_c_width, MARGIN_Y + temp_c_bottom + SPACING - feels_like_c_y_offset),
        feels_like_c, font=large_font, fill=BLACK)
    print("feels_like_c_bottom: " + str(feels_like_c_bottom))

    feels_like_f_num = _get_fahrenheit(feels_like_c_num)
    feels_like_f = "%d°F" % round(feels_like_f_num)
    feels_like_f_bbox = large_font.getbbox(feels_like_f)
    feels_like_f_y_offset = feels_like_f_bbox[1]
    feels_like_f_width = feels_like_f_bbox[2]
    feels_like_f_bottom = MARGIN_Y + temp_f_bottom + SPACING + feels_like_f_bbox[3] - feels_like_f_y_offset
    draw.text(
        (config.WIDTH - full_temp_c_width - feels_like_f_width, MARGIN_Y + temp_f_bottom + SPACING - feels_like_f_y_offset),
        feels_like_f, font=large_font, fill=BLACK)
    print("feels_like_f_bottom: " + str(feels_like_f_bottom))

    (font_width, font_height) = _get_size(small_font.getbbox("feels"))
    xy = (config.WIDTH - font_width - full_temp_both_width, feels_like_f_bottom - feels_like_f_bbox[3])
    draw.text(xy, "feels", font=small_font, fill=BLACK)
    feels_font_height = font_height

    (font_width, font_height) = _get_size(small_font.getbbox("like"))
    xy = (config.WIDTH - font_width - full_temp_both_width, feels_like_f_bottom - feels_like_f_bbox[3] + feels_font_height)
    draw.text(xy, "like", font=small_font, fill=BLACK)

    humidity = "%d%%" % weather["main"]["humidity"]
    (font_width, font_height) = _get_size(large_font.getbbox(humidity))
    xy = (config.WIDTH - font_width, feels_like_f_bottom)
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
    """

    return image


def get_page(page_index):
    page_config = config.CONFIG_PAGES[page_index]
    weather = data.get_weather(page_config['lat'], page_config['long'])
    if not weather:
        return None
    return _display_weather(page_config['label'], weather)
