class Score(object):
    """Represents total user score
    """
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

    def update(self, n):
        """Update the score according to the length of the chain

        :param n: int chain length
        :return: total number of points
        """
        if n < 2:
            raise ValueError("Minimum chain number must be 2, got <{0}>".format(n))
        self.points += (n-1)*5
        return self.points
