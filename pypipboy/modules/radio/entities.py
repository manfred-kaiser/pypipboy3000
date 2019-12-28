import os
from pypipboy import game
from pypipboy import config
import pygame

from random import choice


class RadioStation(game.Entity):

    STATES = {
        'stopped': 0,
        'playing': 1,
        'paused': 2
    }

    def __init__(self, configfile, section, *args, **kwargs):
        super(RadioStation, self).__init__((10, 10), *args, **kwargs)
        self.configfile = configfile
        self.section = section
        self.state = self.STATES['stopped']
        self.files = self.load_files()
        pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])

    @property
    def directory(self):
        return self.configfile.get(self.section, 'directory')

    @property
    def name(self):
        return self.configfile.get(self.section, 'name')

    def play_random(self):
        if not self.files:
            return
        f = choice(self.files)
        self.filename = f
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        self.state = self.STATES['playing']

    def play(self):
        if self.state == self.STATES['paused']:
            pygame.mixer.music.unpause()
            self.state = self.STATES['playing']
        else:
            self.play_random()

    def pause(self):
        self.state = self.STATES['paused']
        pygame.mixer.music.pause()

    def stop(self):
        self.state = self.STATES['stopped']
        pygame.mixer.music.stop()

    def load_files(self):
        files = []
        for f in os.listdir(self.directory) if self.directory else []:
            if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
                files.append(os.path.join(self.directory, f))
        return files
