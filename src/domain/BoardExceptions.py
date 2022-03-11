class ColumnOverflowException(Exception):
    def __init__(self, msg_):
        self._msg = msg_

class InvalidColumnException(Exception):
    def __init__(self, msg_):
        self._msg = msg_