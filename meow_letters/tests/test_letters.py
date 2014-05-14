import unittest

from meow_letters.letters import Letter, LetterChain


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

    def test_next(self):
        letter_g = Letter('G')
        self.assertEqual(letter_g.next, Letter("H"))
        letter_z = Letter('Z')
        self.assertIsNone(letter_z.next)

    def test_previous(self):
        letter_g = Letter('G')
        self.assertEqual(letter_g.previous, Letter("F"))
        letter_a = Letter('A')
        self.assertIsNone(letter_a.previous)

    def test_adjacent(self):
        letter_a = Letter('A')
        self.assertEqual(letter_a.adjacent, [None, Letter("B")])
        letter_t = Letter("T")
        self.assertEqual(letter_t.adjacent, [Letter("S"), Letter("U")])
        letter_z = Letter("Z")
        self.assertEqual(letter_z.adjacent, [Letter("Y"), None])

    def test_any_adjacent(self):
        letter_a = Letter('A')
        self.assertEqual(letter_a.any_adjacent, Letter("B"))
        letter_t = Letter("T")
        self.assertIn(letter_t.any_adjacent, [Letter("U"), Letter("S")])
        letter_z = Letter("Z")
        self.assertEqual(letter_z.any_adjacent, Letter("Y"))

    def test_is_first(self):
        letter_a = Letter("A")
        self.assertTrue(letter_a.is_first())
        letter_p = Letter("P")
        self.assertFalse(letter_p.is_first())

    def test_is_last(self):
        letter_p = Letter("P")
        self.assertFalse(letter_p.is_last())
        letter_z = Letter("Z")
        self.assertTrue(letter_z.is_last())

    def test_get_next_letters(self):
        letter_a = Letter("A")
        self.assertEqual(letter_a.get_next_letters(1), [Letter("B")])
        self.assertEqual(letter_a.get_next_letters(2), [Letter("B"), Letter("C")])
        letter_y = Letter("Y")
        self.assertEqual(letter_y.get_next_letters(1), [Letter("Z")])
        self.assertIsNone(letter_y.get_next_letters(2))
        self.assertRaises(ValueError, letter_y.get_next_letters, 0)

    def test_get_adjacent_letters(self):
        letter_a = Letter("A")
        letter_z = Letter("Z")
        self.assertRaises(ValueError, letter_a.get_adjacent_letters, 0)
        self.assertRaises(ValueError, letter_a.get_adjacent_letters, 27)
        self.assertEqual(letter_a.get_adjacent_letters(3), [letter_a, Letter("B"), Letter("C")])
        self.assertEqual(letter_z.get_adjacent_letters(3), [Letter("X"), Letter("Y"), letter_z])

        letter_b = Letter("B")
        adjacents = letter_b.get_adjacent_letters(6)
        self.assertEqual(len(adjacents), 6)
        for a in adjacents:
            self.assertIn(a, [letter_a, letter_b, Letter("C"), Letter("D"),
                              Letter("E"), Letter("F"), Letter("G")])

        letter_h = Letter("H")
        adjacents = letter_h.get_adjacent_letters(3)
        self.assertEqual(len(adjacents), 3)
        for a in adjacents:
            self.assertIn(a, [Letter("F"), Letter("G"), letter_h, Letter("I"), Letter("J")])


class TestLetterChain(unittest.TestCase):
    def setUp(self):
        self.chain = LetterChain()

    def test_add(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        self.chain.add(letter_a)
        self.assertEqual(self.chain.chain, [letter_a])
        self.chain.add(letter_b)
        self.assertEqual(self.chain.chain, [letter_a, letter_b])

    def test_remove(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        letter_c = Letter("C")
        self.assertRaises(ValueError, self.chain.remove, letter_a)
        self.chain.set_chain([letter_a, letter_b, letter_c])
        self.assertRaises(ValueError, self.chain.remove, Letter("Z"))
        self.chain.remove(letter_c)
        self.assertEqual(self.chain.get_chain(), [letter_a, letter_b])
        self.chain.add(letter_c)
        self.chain.remove(letter_b)
        self.assertEqual(self.chain.get_chain(), [letter_a])
        self.chain.set_chain([letter_a, letter_b, letter_c])
        self.chain.remove(letter_a)
        self.assertEqual(self.chain.get_chain(), [])

    def test_length(self):
        self.assertEqual(self.chain.length, 0)
        self.chain.add(Letter("A"))
        self.assertEqual(self.chain.length, 1)
        self.chain.add(Letter("B"))
        self.assertEqual(self.chain.length, 2)

    def test_is_valid(self):
        letter_a = Letter("A")
        letter_b = Letter("B")
        letter_d = Letter("D")
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_a)
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_b)
        self.assertTrue(self.chain.is_valid())
        self.chain.add(letter_d)
        self.assertFalse(self.chain.is_valid())
        self.chain.chain = [letter_a, letter_a]
        self.assertFalse(self.chain.is_valid())


if __name__ == '__main__':
    unittest.main()
