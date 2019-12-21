from pypipboy.pypboy import BaseModule
from pypipboy.pypboy.modules.stats import status
from pypipboy.pypboy.modules.stats import special
from pypipboy.pypboy.modules.stats import skills
from pypipboy.pypboy.modules.stats import perks
from pypipboy.pypboy.modules.stats import general


class Module(BaseModule):

	label = "STATS"
	GPIO_LED_ID = 30 #GPIO 22 #19

	def __init__(self, *args, **kwargs):
		self.submodules = [
			status.Module(self),
			special.Module(self),
			skills.Module(self),
			perks.Module(self),
			general.Module(self)
		]
		super(Module, self).__init__(*args, **kwargs)
