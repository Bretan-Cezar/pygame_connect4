import os
from service.Service import Service
from domain.BoardExceptions import *
from service.ServiceExceptions import *

class UI:

    def __init__(self):

        self._service = None

    def _read_board_size(self):

        os.system('cls')
        print("Welcome to Connect Four! Enter the game's board size:")

        rows = 0
        while rows < 5 or rows > 9:
            
            rows = input("No. of rows (min. 5, max. 9): ")
            try:
                rows = int(rows)
            except ValueError:
                rows = 0
        
        cols = 0
        while cols < 5 or cols > 9:
            
            cols = input("No. of columns (min. 5, max. 9): ")
            try:
                cols = int(cols)
            except ValueError:
                cols = 0
        
        return Service(rows, cols)

    def start(self):
        
        os.system('cls')

        self._service = self._read_board_size()

        done = False
        while not done:
            
            os.system('cls')
            print(self._service.printable_board())

            valid_input = False
            while not valid_input:

                col_push = ' '
                while not isinstance(col_push, int):
                    
                    col_push = input("Enter the column where you want to drop a coin: ")
                    try:
                        col_push = int(col_push)
                    except ValueError:
                        print('Column must be a number!')
                        col_push = ' '
            
                try:
                    self._service.player_push_to_col(col_push)
                    valid_input = True
                except ColumnOverflowException as coe:
                    print(str(coe))
                except InvalidColumnException as ice:
                    print(str(ice))
            
            if self._service.check_winner() != None:
                done = True
                os.system('cls')
                print(self._service.printable_board())
                print('Player wins!')

            else:
                
                try:
                    self._service.check_draw()
                except DrawException as de:
                    os.system('cls')
                    print(self._service.printable_board())
                    print(str(de))
                    break

                self._service.computer_push_to_col()
                
                try:
                    self._service.check_draw()
                except DrawException as de:
                    os.system('cls')
                    print(self._service.printable_board())
                    print(str(de))
                    break

                if self._service.check_winner() != None:
                    done = True
                    os.system('cls')
                    print(self._service.printable_board())
                    print('Computer wins!')                
