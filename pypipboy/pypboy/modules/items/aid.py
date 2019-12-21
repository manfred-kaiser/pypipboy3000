from pypipboy import pypboy
import pygame
from pypipboy import game
from pypipboy import config


class Module(pypboy.SubModule):

	label = "Aid"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)