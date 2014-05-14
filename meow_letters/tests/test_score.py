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

    def test_update(self):
        self.assertEqual(self.score.update(2), 5)
        self.assertEqual(self.score.update(3), 15)
        self.assertEqual(self.score.update(5), 35)


if __name__ == '__main__':
    unittest.main()
