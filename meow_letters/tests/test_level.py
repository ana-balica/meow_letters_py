import unittest

from meow_letters.level import Level

class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level = Level()

    def test_up(self):
        self.assertRaises(ValueError, self.level.set_level, -1)
        self.assertEqual(self.level.set_level(50), 1)
        self.assertEqual(self.level.set_level(130), 2)
        self.assertEqual(self.level.set_level(490), 5)

if __name__ == '__main__':
    unittest.main()
