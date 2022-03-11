import os
from ui.UI import UI
from ui.GUI import GUI
from service.test_Service import TestService
from domain.test_Board import TestBoard

os.system('cls')
_mode = input('ENTER MODE (ui / gui / anything else to exit): ')

# Test instances go here

test_board = TestBoard()
test_service = TestService()

test_board.execute()
test_service.execute()

if _mode == "ui":

    _ui = UI()
    _ui.start()

elif _mode == "gui":

    _gui = GUI()
    _gui.start()
