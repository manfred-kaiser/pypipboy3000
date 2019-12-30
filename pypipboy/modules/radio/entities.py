import os
from random import choice
import pygame
from pypipboy.game.core import Entity


class RadioStation(Entity):

    STATES = {
        'stopped': 0,
        'playing': 1,
        'paused': 2
    }

    def __init__(self, pipboy, section, event):
        super(RadioStation, self).__init__((10, 10))
        self.pipboy = pipboy
        self.section = section
        self.state = self.STATES['stopped']
        self.files = self.load_files()
        pygame.mixer.music.set_endevent(event)

    @property
    def directory(self):
        return self.pipboy.configfile.get(self.section, 'directory')

    @property
    def name(self):
        return self.pipboy.configfile.get(self.section, 'name')

    def play_random(self):
        if not self.files:
            return
        filename = choice(self.files)  # nosec
        pygame.mixer.music.load(filename)
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
