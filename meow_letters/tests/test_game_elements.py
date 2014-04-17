import unittest

from meow_letters.game_elements import Letter


class TestLetter(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, Letter)
        self.assertRaises(ValueError, Letter, 1)
        letter = Letter('A')
        self.assertEqual(letter.letter, 'A')
        self.assertFalse(letter.selected)

    def test_selection(self):
        letter = Letter('A')
        self.assertFalse(letter.selected)
        self.assertFalse(letter.is_selected())
        letter.select()
        self.assertTrue(letter.selected)
        self.assertTrue(letter.is_selected())
        letter.unselect()
        self.assertFalse(letter.selected)
        self.assertFalse(letter.is_selected())


if __name__ == '__main__':
    unittest.main()
