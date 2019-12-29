from pypipboy import pypboy

from pypipboy.pypboy.ui import MenuItem


class Module(pypboy.SubModule):

    LABEL = "S.P.E.C.I.A.L."
    headline = "STATUS"
    title = " HP 160/175  |  AP 62/62"

    def __init__(self, parent, configfile=None):
        super(Module, self).__init__(parent, configfile)
        self.menu.add_item(MenuItem("CND"))
