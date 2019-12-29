import pygame
from pypipboy import pypboy
from pypipboy import config

from pypipboy.modules.radio import entities
from pypipboy.pypboy.ui import MenuItem


class RadioModule(pypboy.SubModule):

    LABEL = "Radio"
    EVENT_SONG_END = pygame.USEREVENT + 1

    def __init__(self, *args, **kwargs):
        super(RadioModule, self).__init__(*args, **kwargs)
        self.parent.pypboy.register_event(self.EVENT_SONG_END, self.handle_event)
        self.stations = {}
        for section in self.parent.pypboy.configfile.sections():
            if section.startswith('Radio:'):
                radio_station = entities.RadioStation(
                    configfile=self.parent.pypboy.configfile,
                    section=section,
                    event=self.EVENT_SONG_END
                )
                self.stations[radio_station.name] = radio_station
                self.add(radio_station)
                self.menu.add_item(MenuItem(radio_station.name, self.select_station))

        self.active_station = None

    def select_station(self, menuitem):
        if self.active_station:
            self.active_station.stop()
        self.active_station = self.stations[menuitem.title]
        self.active_station.play_random()

    def handle_event(self, event):
        if event.type == self.EVENT_SONG_END:
            if self.active_station:
                self.active_station.play_random()
