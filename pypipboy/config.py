import os
from collections import defaultdict
import pkg_resources
import pygame


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ImportError:
    pass


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


class ActionManager():

    class ActionNotUnique(Exception):
        pass

    class ActionItem():

        def __init__(self, key, callback, params=None, unique=False):
            self.key = key
            self.callback = callback
            self.params = params or []
            self.unique = unique

        def call(self):
            self.callback(*self.params)

    def __init__(self, configfile):
        self.configfile = configfile
        self._actions = defaultdict(list)
        self._gpio_mapping = {}

    def add_action(self, key, callback, unique=False):
        action_item = ActionManager.ActionItem(key, callback, unique)
        if action_item.unique:
            for item in self._actions[key]:
                if item.unique:
                    raise ActionManager.ActionNotUnique()
        self._actions[key].append(action_item)

    def add_gpio_mapping(self, pin, key):
        self._gpio_mapping[pin] = key

    def handle_action(self, event):
        if event.key in self._actions:
            for item in self._actions[event.key]:
                item.call()
            return True
        return False


class SoundManager():

    def __init__(self, configfile):
        self.configfile = configfile
        self._sound_enabled = True
        self._sounds = {}
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
        except Exception:
            self._sound_enabled = False

    def play(self, sound_name):
        if self._sound_enabled:
            if sound_name not in self._sounds:
                sound_filename = self.configfile.get('SOUND:FILES', sound_name)
                if not os.path.isfile(sound_filename):
                    sound_filename = pkg_resources.resource_filename('pypipboy', sound_filename)
                self._sounds[sound_name] = pygame.mixer.Sound(sound_filename)
            self._sounds[sound_name].play()


class FontManager():

    def __init__(self):
        pygame.font.init()
        self._fonts = {}

    def __getitem__(self, fontsize):
        if fontsize not in self._fonts:
            self._fonts[fontsize] = pygame.font.Font(
                pkg_resources.resource_filename(
                    'pypipboy',
                    'data/monofonto.ttf'
                ),
                fontsize
            )
        return self._fonts[fontsize]
