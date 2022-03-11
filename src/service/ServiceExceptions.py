class DrawException(Exception):
    def __init__(self, msg_):
        self._msg = msg_