from domain.Board import Board
import random
from service.ServiceExceptions import *

class Service:

    def __init__(self, rows_, cols_):
        
        self._board = Board(rows_, cols_)

    def player_push_to_col(self, col_):
        """
        Service method that calls the Board object's push to column method, and as
        an effect it "drops a player's coin" in the column given as a parameter.
        * The "player's coin" in this case is represented as a yellow lightning bolt unicode symbol.

        @param: col_ - The column where it is needed to push the symbol.
        @return: -
        """
        self._board.push_to_col(col_, '\u26A1')
    
    def computer_push_to_col(self):
        """
        Service method that calls the Board object's push to column method, and as
        an effect it "drops a computer's coin" in a column determined by an algorithm that
        analyzes the current state of the game so that the player is put in difficulty making sequences
        of 4 symbols and also take advantage of opportunities to build longer sequences of symbols.

        @param: -
        @return: -
        """

        matrix = self._board.data

        '''
        Let (x+dirx[i], y+diry[i]) be a tuple that represents a point in the board matrix whose coordinates
        are being offset by a value dictated by the index i from the direction arrays so that the resulting
        coordinates point to one of the points adjacent to (x, y) (except the one right below it).

        0 = left ; 1 = up-left ; 2 = up ; 3 = up-right ; 4 = right ; 5 = down-right ; 6 = down-left
        '''

        dirx = [0, -1, -1, -1, 0, 1, 1]
        diry = [-1, -1, 0, 1, 1, 1, -1]

        '''
        The "degree" may represent the length of the longest sequence currently built by the player or the computer.
        It can be 1, 2, 3, and when there is a possible winning move for the computer it should be 4.
        The possible_moves list that contains column numbers is reset whenever the degree is being increased,
        since it can be considered a "priority number".
        '''

        degree = 1
        possible_moves = [i for i in range(1, self._board.cols + 1)]

        null = chr(32)
        n = self._board.rows
        m = self._board.cols
        sx = n

        '''
        The main algorithm runs on the n x m matrix, and it is a tweaked version of Lee's Algorithm, keeping in mind that:
        - sequences are unidirectional;
        - there must be a symbol underneath the place where a sequence can be prolonged; 
        - there might be a gap within a potential sequence; 
        - if both the player and the computer have a sequence of 3 symbols, the completion priority must be given to the computer's.
        '''
        while sx >= 1:
            
            sy = 1
            while sy <= m:

                if matrix[sx][sy] == null:
                    sy += 1
                
                else:
                    # A potential starting point to a sequence has been found.
                    for i in range(7):
                        # We begin scanning for potential sequences in the direction dictated by i.
                        length = 1
                        x = sx
                        y = sy
                        chain = True
                        while chain:
                            
                            xx = x + dirx[i]
                            yy = y + diry[i]

                            if xx >= 1 and xx <= n and yy >= 1 and yy <= m and matrix[xx][yy] == matrix[x][y]:
                                # A symbol from the same player has been found at the point adjacent to the last point in the direction i.
                                length += 1

                                if xx + dirx[i] >= 1 and xx + dirx[i] <= n and yy + diry[i] >= 1 and yy + diry[i] <= m and matrix[xx + dirx[i]][yy + diry[i]] == null and (xx + dirx[i] == n or matrix[xx + dirx[i] + 1][yy + diry[i]] != null):
                                    # There must be a symbol underneath the place where a sequence can be prolonged.
                                    
                                    if xx + dirx[i] + dirx[i] >= 1 and xx + dirx[i] + dirx[i] <= n and yy + diry[i] + diry[i] >= 1 and yy + diry[i] + diry[i] <= m and matrix[xx][yy] == matrix[xx + dirx[i] + dirx[i]][yy + diry[i] + diry[i]]:
                                        # There might be a gap within a potential sequence.
                                        length += 1

                                    if length == 3 and matrix[xx][yy] == '\u26D4':
                                        # If both the player and the computer have a sequence of 3 symbols, the completion priority must be given to the computer's.
                                        length += 1

                                    if length > degree:
                                        degree = length
                                        possible_moves = []
                                        possible_moves.append(yy + diry[i])
                                        chain = False

                                    elif length == degree:
                                        possible_moves.append(yy + diry[i])
                                        chain = False
                                    
                                x = xx
                                y = yy
                            else:
                                chain = False
                    
                    sy += 1
                
            sx -= 1

        '''
        Finally, by picking one of the column numbers from the possible_moves list, while they
        may or may not have the same effect in the long term, they all provide a reasonably
        competitive play. A "computer's coin" being "dropped" on the randomly selected column number.
        '''
        col = random.choice(possible_moves)
        self._board.push_to_col(col, '\u26D4')


    def check_draw(self):
        """
        Service method that checks whether the entire table is filled with symbols.
        Makes use of the Board object's get_current_col_size() method.
        If all the columns have reached their maximum number of symbols,
        DrawException is being raised.
        This method is being called in the UI right before and right after computer's move.

        @param: -
        @return: -
        """
        full = True
        for col in range(1, self._board.cols + 1):
            if self._board.get_current_col_size(col) < self._board.rows:
                full = False
        if full:
            raise DrawException('Draw!')


    def check_winner(self):
        """
        Service method that scans the board's matrix for sequences of 4 of the same symbols.
        If no sequence of this kind is found, the function returns None, otherwise it
        returns the symbol that forms the sequence.
        This is also determined by a tweaked version of Lee's Algorithm, but much simpler
        than the one implemented in the computer strategy method.

        @param: -
        @return: None / Symbol
        """

        matrix = self._board.data

        '''
        0 = up-left, 1 = up ; 2 = up-right ; 3 = right
        '''

        dirx = [-1, -1, -1, 0]
        diry = [-1, 0, 1, 1]
        
        null = chr(32)
        n = self._board.rows
        m = self._board.cols
        sx = n
        
        while sx >= 1:
            
            sy = 1
            while sy <= m:

                if matrix[sx][sy] == null:
                    sy += 1
                
                else:

                    for i in range(4):
                        length = 1
                        x = sx
                        y = sy
                        chain = True
                        while chain:
                            
                            xx = x + dirx[i]
                            yy = y + diry[i]

                            if xx >= 1 and yy >= 1 and yy <= m and matrix[xx][yy] == matrix[x][y]:
                                length += 1
                                if length == 4:
                                    return matrix[xx][yy]
                                x = xx
                                y = yy
                            else:
                                chain = False
                    
                    sy += 1
                
            sx -= 1

        return None


    def printable_board(self):
        """
        Service method that returns the board's matrix in a printable form.
        """
        return str(self._board)

    def board_matrix(self):

        return self._board.data