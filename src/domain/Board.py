from texttable import Texttable
from domain.BoardExceptions import *

class Board:

    def __init__(self, rows_, cols_):
        """
        Constructor for Board class.
        Initializes a bidimensional list of dimensions rows_ x cols_ with null characters, representing that the given position
        does not contain any symbols, which are, in practice, coins dropped by players.

        @param: rows_ - Number of rows on the board given from the UI, where it's checked that it is >= 5 and <= 9.
                cols_ - Number of columns on the board given from the UI, where it's checked that it is >= 5 and <= 9.
        """
        self._rows = rows_
        self._cols = cols_
        self._data = [[chr(32) for i in range(cols_ + 1)] for j in range(rows_ + 1)]
    
    '''
    Getters for the Board class.
    '''
    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def data(self):
        return self._data


    def get_current_col_size(self, col_):
        """
        Method that returns the number of symbols representing coins dropped by players in a given column.

        @param: col_ - The column whose number of symbols within it must be returned.
        @return: The number of symbols within the given column.
        """
        _size = 0
        row = self._rows
        while self._data[row][col_] != chr(32) and row > 0:
            _size += 1
            row -= 1
        
        return _size


    def push_to_col(self, col_, char_):
        """
        Method that "drops a player coin" in a column.
        The n x m bidimensional list can be viewed as m stacks with a maximum amount of n symbols within them.
        If the given column number is not inclusively between 1 and m, InvalidColumnException is being raised.
        If pushing a symbol to a "full" column is being attempted, ColumnOverflowException is being raised.

        @param: col_ - The column where it is needed to push the symbol.
                char_ - The symbol that needs to be pushed.
        @return: -
        """
        if col_ < 1 or col_ > self._cols:
            raise InvalidColumnException('Entered column is out of bounds!')

        if self.get_current_col_size(col_) == self._rows:
            raise ColumnOverflowException('This column is full!')

        self._data[self._rows - self.get_current_col_size(col_)][col_] = char_

    def __str__(self):
        """
        str() operator overriding method.
        Returns the bidimensional list in a printable form via the Texttable class.
        The values of the bidimensional list are being placed in a table-like whole string,
        and a header that indicates the column numbers is being placed above them.

        @param: - 
        @return: The bidimensional list in the printable format described above.
        """
        table = Texttable()
        _header = [chr(49+i) for i in range(self._cols)]
        table.header(_header)
        for i in range(1, self._rows + 1):
            table.add_row(self._data[i][1:])
        
        return table.draw()
