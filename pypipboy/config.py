import os
from configparser import ConfigParser
import pkg_resources
import pygame

try:
    pygame.mixer.init(44100, -16, 2, 2048)
    SOUND_ENABLED = True
except Exception:
    SOUND_ENABLED = False


CONFIGFILE = ConfigParser(allow_no_value=True)
CONFIGFILE.read(pkg_resources.resource_filename('pypipboy', 'data/default.ini'))

WIDTH = CONFIGFILE.getint('Display', 'width')
HEIGHT = CONFIGFILE.getint('Display', 'height')


MAP_FOCUS = (-102.3016145, 21.8841274)

EVENTS = {
    'SONG_END': pygame.USEREVENT + 1
}

ACTIONS = {
    pygame.K_F1: "module_stats",
    pygame.K_F2: "module_items",
    pygame.K_F3: "module_data",
    pygame.K_1: "knob_1",
    pygame.K_2: "knob_2",
    pygame.K_3: "knob_3",
    pygame.K_4: "knob_4",
    pygame.K_5: "knob_5",
    pygame.K_UP: "dial_up",
    pygame.K_DOWN: "dial_down"
}


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ImportError:
    pass

GPIO_AVAILABLE = CONFIGFILE.getboolean('GPIO', 'enabled')

# Using GPIO.BCM as mode
GPIO_ACTIONS = {
    4: "module_stats",  # GPIO 4
    14: "module_items",  # GPIO 14
    15: "module_data",  # GPIO 15
    17: "knob_1",  # GPIO 17
    18: "knob_2",  # GPIO 18
    7: "knob_3",  # GPIO 7
    22: "knob_4",  # GPIO 22
    23: "knob_5",  # GPIO 27
    #    31: "dial_up", # GPIO 23
    27: "dial_down"  # GPIO 7
}


MAP_ICONS = {}
map_icon_path = 'data/images/map_icons'
for icon in pkg_resources.resource_listdir('pypipboy', map_icon_path):
    icon_name = icon.rsplit('.', 1)[0]
    MAP_ICONS[icon_name] = pygame.image.load(pkg_resources.resource_filename(
        'pypipboy', os.path.join(map_icon_path, icon)
    ))

AMENITIES = {key: MAP_ICONS[value] for key, value in CONFIGFILE.items('MAPICONS')}


pygame.font.init()
FONTS = {}
for x in range(10, 28):
    FONTS[x] = pygame.font.Font(pkg_resources.resource_filename(
        'pypipboy', 'data/monofonto.ttf'
    ), x)

radio = None
