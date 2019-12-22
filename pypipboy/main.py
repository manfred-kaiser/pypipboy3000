import pygame
# import os


from pypipboy import config

# Init framebuffer/touchscreen environment variables
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV'      , '/dev/fb1')
# os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
# os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    config.GPIO_AVAILABLE = True
except ImportError:
    print("GPIO UNAVAILABLE")
    config.GPIO_AVAILABLE = False

from pypipboy.pypboy.core import Pypboy
from pypipboy.modules import data
from pypipboy.modules import items
from pypipboy.modules import stats

try:
    pygame.mixer.init(44100, -16, 2, 2048)
    config.SOUND_ENABLED = True
except Exception:
    config.SOUND_ENABLED = False


def main():
    boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)

    boy.add_module('data', data.Module)
    boy.add_module('items', items.Module)
    boy.add_module('stats', stats.Module)

    boy.run('stats')
