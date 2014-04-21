class Score(object):
    def __init__(self, points=0):
        self.points = points

    def add(self, points):
        """Add points to the score

        :param points: int number of points to add
        :return: int number of total points
        """
        if int(points) < 0:
            raise ValueError("The number of point must a positive integer, "
                             "got <{0}>".format(points))
        self.points += int(points)
        return self.points

