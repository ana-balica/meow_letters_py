import random
import itertools

from meow_letters.data.alphabets import ENGLISH_ALPHABET as ALPHABET


class Letter(object):
    """Represents a single letter from the game
    """
    def __init__(self, letter):
        """Letter class initializer

        :param letter: valid string letter from an alphabet
        """
        if not isinstance(letter, basestring):
            raise ValueError("Letter class should be initialized with a basestring, \
                received type <{0}>".format(type(letter)))
        self.letter = letter.upper()
        self.selected = False

    def __repr__(self):
        return "<Letter '{0}' at {1}>".format(self.letter, hex(id(self)))

    def __cmp__(self, other):
        if self.letter < other.letter:
            return -1
        elif self.letter == other.letter:
            return 0
        else:
            return 1

    def select(self):
        """Mark a letter as being selected
        """
        self.selected = True

    def unselect(self):
        """Mark a letter as being unselected
        """
        self.selected = False

    def is_selected(self):
        """Check the state of the letter

        :return: True if the letter is selected, False otherwise
        """
        return self.selected

    @property
    def next(self):
        """Get the next letter in the alphabet

        :return: the next Letter object in the alphabet or None if it's the last
                 letter
        """
        if self.letter == ALPHABET[-1]:
            return None
        i = ALPHABET.index(self.letter)
        return Letter(ALPHABET[i+1])

    @property
    def previous(self):
        """Get the previous letter in the alphabet

        :return: the previous Letter object in the alphabet or None if it's the
                 first letter
        """
        if self.letter == ALPHABET[0]:
            return None
        i = ALPHABET.index(self.letter)
        return Letter(ALPHABET[i-1])

    @property
    def adjacent(self):
        """Get adjacent letters from the alphabet

        :return: list containing 2 Letter objects - the previous and the next;
                 if there is no next or previous, the value is set to None
        """
        return [self.previous, self.next]

    def get_next_letters(self, n):
        """Get a list of n next letters

        :param n: int number of next letter
        :return: list of letters or None if the requested number of letters is too big
        """
        if n < 1:
            raise ValueError("The requested number of next letters must be a "
                             "positive integer, received <{0}>".format(n))
        i = ALPHABET.index(self.letter)
        if i+n >= len(ALPHABET):
            return None
        return [Letter(l) for l in ALPHABET[i+1:i+n+1]]


class LetterBoard(object):
    """Represents all available letters on the board
    """
    def __init__(self, letters=[]):
        """LetterBoard class initializer

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        """
        self.letters = set(letters)

    def setup(self):
        """Initializes the board with 5 random letters with a precomputed adjacent 
        pair of letters

        :return: the current instance
        """
        pass

    def clear(self):
        """Clear the board of letters

        :return: the current instance
        """
        self.letters.clear()
        return self

    def add_letters(self, letters):
        """Add some letters to the board

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :return: the current instance
        """
        letters = set(letters)
        self.letters.update(letters)
        return self

    def remove_letters(self, letters):
        """Remove some letters from the board

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :return: the current instance
        """
        letters = set(letters)
        for letter in letters:
            self.letters.remove(letter)
        return self

    def find_adjacent_letters(self, n, gap=0):
        """Find n number of adjacent letters with a possible gap between them. 
        For instance, 2 letters with a gap of value 1 are 'A' and 'C'; or 3 letters
        with no gap between them are 'X', 'Y' and 'Z'.

        :param n: int number of adjacent letters to be found on the board
        :param gap: int total gap between letters
        :return: list of non-duplicate lists with consecutive ordered letter string
        """
        if n < 2:
            raise ValueError("The minimum number of letters to build a chain is 2, \
                             received <{0}>".format(n))
        if gap < 0:
            raise ValueError("The gap must a be positive int, received <{0}>".format(gap))

        adjacent_combinations = []
        text_letters = {l.letter for l in self.letters}
        letters = list(self.letters)
        letters.sort()
        letters = [i for i, _ in itertools.groupby(letters)]
        for letter in letters:
            next_letters = letter.get_next_letters(n-1)
            if all(l.letter in text_letters for l in next_letters):
                combination = [letter.letter] + [i.letter for i in next_letters]
                adjacent_combinations.extend([combination])

        return adjacent_combinations

    def get_adjacent_letters(self, letters, chain=2):
        """Return adjacent letters in respect to the available letters

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        :param chain: int length of the required final chain to form
        :return: list of adjacent letter objects
        """
        pass
