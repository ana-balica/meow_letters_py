import unittest

from meow_letters.score import Score

class TestScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def test_add(self):
        self.assertRaises(ValueError, self.score.add, -1)
        self.score.add(15)
        self.assertEqual(self.score.points, 15)
        self.score.add(0)
        self.assertEqual(self.score.points, 15)
        self.score.add(30)
        self.assertEqual(self.score.points, 45)

if __name__ == '__main__':
    unittest.main()
