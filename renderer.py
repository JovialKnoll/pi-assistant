from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

import config


# drawing vars
ICON_MAP = {
    '01d': 'B',
    '01n': 'C',
    '02d': 'H',
    '02n': 'I',
    '03d': 'N',
    '03n': 'N',
    '04d': 'Y',
    '04n': 'Y',
    '09d': 'Q',
    '09n': 'Q',
    '10d': 'R',
    '10n': 'R',
    '11d': 'Z',
    '11n': 'Z',
    '13d': 'W',
    '13n': 'W',
    '50d': 'J',
    '50n': 'K',
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MARGIN_X = 0
MARGIN_Y = 1
SPACING = 1
small_font = ImageFont.truetype(
    Path(__file__).parent / 'fonts' / 'dejavu' / 'DejaVuSans-Bold.ttf',
    16)
medium_font = ImageFont.truetype(
    Path(__file__).parent / 'fonts' / 'dejavu' / 'DejaVuSans.ttf',
    20)
large_font = ImageFont.truetype(
    Path(__file__).parent / 'fonts' / 'dejavu' / 'DejaVuSans-Bold.ttf',
    24)
icon_font = ImageFont.truetype(
    Path(__file__).parent / 'fonts' / 'meteocons.ttf',
    54)

example_text = "XxYyPpQqGgJj"
small_font_example_bbox = small_font.getbbox(example_text)
small_font_example_height = small_font_example_bbox[3] - small_font_example_bbox[1]
medium_font_example_bbox = medium_font.getbbox(example_text)
medium_font_example_height = medium_font_example_bbox[3] - medium_font_example_bbox[1]
large_font_example_bbox = large_font.getbbox(example_text)
large_font_example_height = large_font_example_bbox[3] - large_font_example_bbox[1]
full_temp_c_width = large_font.getbbox("-00°C")[2]
full_temp_both_width = full_temp_c_width + large_font.getbbox("100°F")[2]


def _get_celsius(kelvin):
    return kelvin - 273.15


def _get_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def get_weather_display(label, date, weather):
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
    #description_height = description_bbox[3] - description_y_offset
    description_top = config.HEIGHT - MARGIN_Y - small_font_example_height
    draw.text(
        (MARGIN_X, description_top - description_y_offset),
        description, font=small_font, fill=BLACK)
    print("description_top: " + str(description_top))

    main = weather["weather"][0]["main"]
    main_bbox = large_font.getbbox(main)
    main_y_offset = main_bbox[1]
    #main_height = main_bbox[3] - main_y_offset
    main_top = description_top - SPACING - large_font_example_height
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
        (MARGIN_X + SPACING, icon_top - icon_y_offset),
        icon, font=icon_font, fill=BLACK)

    temp_c_num = _get_celsius(weather["main"]["temp"])
    temp_c = "%d°C" % round(temp_c_num)
    temp_c_bbox = large_font.getbbox(temp_c)
    temp_c_y_offset = temp_c_bbox[1]
    temp_c_width = temp_c_bbox[2]
    temp_c_bottom = MARGIN_Y + temp_c_bbox[3] - temp_c_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - temp_c_width, temp_c_bottom - temp_c_bbox[3]),
        temp_c, font=large_font, fill=BLACK)
    print("temp_c_bottom: " + str(temp_c_bottom))

    temp_f_num = _get_fahrenheit(temp_c_num)
    temp_f = "%d°F" % round(temp_f_num)
    temp_f_bbox = large_font.getbbox(temp_f)
    temp_f_y_offset = temp_f_bbox[1]
    temp_f_width = temp_f_bbox[2]
    temp_f_bottom = MARGIN_Y + temp_f_bbox[3] - temp_f_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - full_temp_c_width - temp_f_width, temp_f_bottom - temp_f_bbox[3]),
        temp_f, font=large_font, fill=BLACK)
    print("temp_f_bottom: " + str(temp_f_bottom))

    feels_like_c_num = _get_celsius(weather["main"]["feels_like"])
    feels_like_c = "%d°C" % round(feels_like_c_num)
    feels_like_c_bbox = large_font.getbbox(feels_like_c)
    feels_like_c_y_offset = feels_like_c_bbox[1]
    feels_like_c_width = feels_like_c_bbox[2]
    feels_like_c_bottom = temp_c_bottom + SPACING + feels_like_c_bbox[3] - feels_like_c_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - feels_like_c_width, feels_like_c_bottom - feels_like_c_bbox[3]),
        feels_like_c, font=large_font, fill=BLACK)
    print("feels_like_c_bottom: " + str(feels_like_c_bottom))

    feels_like_f_num = _get_fahrenheit(feels_like_c_num)
    feels_like_f = "%d°F" % round(feels_like_f_num)
    feels_like_f_bbox = large_font.getbbox(feels_like_f)
    feels_like_f_y_offset = feels_like_f_bbox[1]
    feels_like_f_width = feels_like_f_bbox[2]
    feels_like_f_bottom = temp_f_bottom + SPACING + feels_like_f_bbox[3] - feels_like_f_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - full_temp_c_width - feels_like_f_width, feels_like_f_bottom - feels_like_f_bbox[3]),
        feels_like_f, font=large_font, fill=BLACK)
    print("feels_like_f_bottom: " + str(feels_like_f_bottom))

    feels_bbox = small_font.getbbox("feels")
    feels_y_offset = feels_bbox[1]
    feels_width = feels_bbox[2]
    feels_bottom = temp_f_bottom + SPACING + feels_bbox[3] - feels_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - full_temp_both_width - feels_width, feels_bottom - feels_bbox[3]),
        "feels", font=small_font, fill=BLACK)
    print("feels_bottom: " + str(feels_bottom))

    like_bbox = small_font.getbbox("like")
    like_y_offset = like_bbox[1]
    like_width = like_bbox[2]
    like_bottom = feels_bottom + SPACING + like_bbox[3] - like_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - full_temp_both_width - like_width, like_bottom - like_bbox[3]),
        "like", font=small_font, fill=BLACK)
    print("like_bottom: " + str(like_bottom))

    humidity = "%d%%" % weather["main"]["humidity"]
    humidity_bbox = large_font.getbbox(humidity)
    humidity_y_offset = humidity_bbox[1]
    humidity_width = humidity_bbox[2]
    humidity_bottom = feels_like_c_bottom + SPACING + humidity_bbox[3] - humidity_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - humidity_width, humidity_bottom - humidity_bbox[3]),
        humidity, font=large_font, fill=BLACK)
    print("humidity_bottom: " + str(humidity_bottom))

    wind_speed = "%dm/s" % weather["wind"]["speed"]
    wind_speed_bbox = large_font.getbbox(wind_speed)
    wind_speed_y_offset = wind_speed_bbox[1]
    wind_speed_width = wind_speed_bbox[2]
    wind_speed_bottom = humidity_bottom + SPACING + wind_speed_bbox[3] - wind_speed_y_offset
    draw.text(
        (config.WIDTH - MARGIN_X - wind_speed_width, wind_speed_bottom - wind_speed_bbox[3]),
        wind_speed, font=large_font, fill=BLACK)
    print("wind_speed_bottom: " + str(wind_speed_bottom))

    wind_deg = weather["wind"]["deg"]
    wind_radians = math.radians((270 - wind_deg) % 360)
    midway = (config.HEIGHT - wind_speed_bottom) // 2
    center = (config.WIDTH - midway, config.HEIGHT - midway)
    radius = config.HEIGHT - 1 - MARGIN_Y - center[1]
    draw.circle(center, radius, outline=BLACK)
    draw.point((
        (center[0], center[1] - radius - 1),
        (center[0], center[1] - radius + 1),
        (center[0], center[1] + radius + 1),
        (center[0], center[1] + radius - 1),
        (center[0] - radius - 1, center[1]),
        (center[0] - radius + 1, center[1]),
        (center[0] + radius + 1, center[1]),
        (center[0] + radius - 1, center[1]),
        ), fill=BLACK)
    draw.line((
        center,
        (center[0] - radius * math.cos(wind_radians), center[1] + radius * math.sin(wind_radians)),
        ), fill=BLACK)

    month_day = date.strftime("%m-%d")
    month_day_bbox = large_font.getbbox(month_day)
    month_day_y_offset = month_day_bbox[1]
    month_day_width = month_day_bbox[2]
    month_day_top = config.HEIGHT - MARGIN_Y - month_day_bbox[3]
    draw.text(
        (center[0] - radius - 1 - SPACING - month_day_width, month_day_top),
        month_day, font=large_font, fill=BLACK)
    print("month_day_top: " + str(month_day_top))

    year = date.strftime("%Y-")
    year_bbox = large_font.getbbox(year)
    year_y_offset = year_bbox[1]
    year_width = year_bbox[2]
    year_top = month_day_top - SPACING - month_day_bbox[3]
    draw.text(
        (center[0] - radius - 1 - SPACING - year_width, year_top),
        year, font=large_font, fill=BLACK)
    print("year_top: " + str(year_top))

    return image
