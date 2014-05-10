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

    def set_level(self, points):
        """Set level according to the number of points a user has

        :param points: int total number of points a user has
        :return: int level
        """
        if points < 0:
            raise ValueError("Number of points must be a positive integer, "
                             "got <{0}>".format(points))
        self.level = int(points/100) + 1
        return self.level

    def reset(self):
        """Reset the level, set level to 1

        :return: the current instance
        """
        self.level = 1
        return self
