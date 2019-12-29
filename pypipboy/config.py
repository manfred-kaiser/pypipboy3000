import os
import pkg_resources
import pygame


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
