# Init framebuffer/touchscreen environment variables
# import os
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV'      , '/dev/fb1')
# os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
# os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

from argparse import ArgumentParser

from pypipboy.pypboy.core import Pypboy
from pypipboy.modules import data
from pypipboy.modules import items
from pypipboy.modules import stats


def main():
    parser = ArgumentParser()
    parser.add_argument('--configfile', help='custom configfile')

    args = parser.parse_args()
    boy = Pypboy(args.configfile)

    boy.add_module('data', data.Module)
    boy.add_module('items', items.Module)
    boy.add_module('stats', stats.Module)

    boy.run('stats')
