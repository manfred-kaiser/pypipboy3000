from pypipboy.pypboy import SubModule
from pypipboy.pypboy.ui import MenuItem


class Module(SubModule):

    LABEL = "S.P.E.C.I.A.L."
    headline = "STATUS"
    title = " HP 160/175  |  AP 62/62"

    def __init__(self, parent):
        super(Module, self).__init__(parent)
        self.menu.add_item(MenuItem("CND"))
