import pygame
from pypipboy.pypboy import SubModule

from pypipboy.modules.radio import entities
from pypipboy.pypboy.ui import MenuItem


class RadioModule(SubModule):

    LABEL = "Radio"
    EVENT_SONG_END = pygame.USEREVENT + 1

    def __init__(self, parent):
        super(RadioModule, self).__init__(parent)
        self.parent.pipboy.register_event(self.EVENT_SONG_END, self.play_next_song)
        self.stations = {}
        for section in self.parent.pipboy.configfile.sections():
            if section.startswith('Radio:'):
                radio_station = entities.RadioStation(
                    pipboy=self.parent.pipboy,
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

    def play_next_song(self, event):
        if self.active_station:
            self.active_station.play_random()
