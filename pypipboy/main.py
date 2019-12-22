# Init framebuffer/touchscreen environment variables
# import os
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV'      , '/dev/fb1')
# os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
# os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

from pypipboy.pypboy.core import Pypboy
from pypipboy.modules import data
from pypipboy.modules import items
from pypipboy.modules import stats


def main():
    boy = Pypboy('Pip-Boy 3000')

    boy.add_module('data', data.Module)
    boy.add_module('items', items.Module)
    boy.add_module('stats', stats.Module)

    boy.run('stats')
