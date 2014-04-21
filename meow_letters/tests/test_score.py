import unittest

from meow_letters.score import Score

class TestScore(unittest.TestCase):
    def setUp(self):
        self.score = Score()

    def test_add(self):
        self.assertRaises(ValueError, self.score.add, -1)
        self.assertEqual(self.score.add(15), 15)
        self.assertEqual(self.score.add(0), 15)
        self.assertEqual(self.score.add(30), 45)

if __name__ == '__main__':
    unittest.main()
