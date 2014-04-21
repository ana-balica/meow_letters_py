class Level(object):
    """Represents user level
    """
    def __init__(self, level=1):
        """Level class initializer

        :param level: int positive number that represents level
        """
        self.level = level

    def __repr__(self):
        return "<Level '{0}' at {1}>".format(self.level, hex(id(self)))
