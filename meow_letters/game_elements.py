import random
import itertools
import collections

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

    @property
    def any_adjacent(self):
        """Return one of the adjacent letters from the alphabet

        :return: Letter object that si adjacent to the current instance
        """
        adjacent = [self.previous, self.next]
        adjacent_filtered = [l for l in adjacent if l is not None]
        return random.choice(adjacent_filtered)

    def is_first(self):
        """Check if the letter is the first in the alphabet

        :return: True if it's first, False otherwise
        """
        return self.letter == ALPHABET[0]

    def is_last(self):
        """Check if the letter is the last in the alphabet

        :return: True if it's last, False otherwise
        """
        return self.letter == ALPHABET[-1]

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

    def get_adjacent_letters(self, n=1):
        """Return adjacent letters in respect to the available letters

        :param n: int length of the required final chain to form
        :return: list of adjacent letter objects ordered consecutively
        """
        if n < 1:
            raise ValueError("Minimum number of chaining is 1, received <{0}>".format(n))
        if n > len(ALPHABET):
            raise  ValueError("Maximum number of chaining it the length of "
                              "alphabet - {0} letters, got <{1}>".format(len(ALPHABET), n))
        if n == 1:
            return [self]
        letters = [self]
        for i in xrange(n-1):
            if letters[0].is_first():
                chosen_letter = letters[-1]
                adjacent = chosen_letter.next
            elif letters[-1].is_last():
                chosen_letter = letters[0]
                adjacent = chosen_letter.previous
            else:
                chosen_letter = random.choice([letters[0], letters[-1]])
                if chosen_letter == letters[0]:
                    adjacent = chosen_letter.previous
                else:
                    adjacent = chosen_letter.next
            if adjacent < chosen_letter:
                letters.insert(0, adjacent)
            else:
                letters.append(adjacent)
        return letters


class LetterChain(object):
    """Represents a chain of letters where order matters

    """
    def __init__(self, chain=[]):
        """LetterChain class initializer

        :param chain: ordered iterable data structure (i.e. list) of Letter objects
        """
        self.chain = list(chain)

    def set_chain(self, chain):
        """Set the chain attribute

        :param chain: ordered iterable data structure (i.e. list) of Letter objects
        :return: the current instance
        """
        self.chain = list(chain)
        return self

    def get_chain(self):
        """Get the chain attribute

        :return: list of Letter objects
        """
        return self.chain

    def add(self, letter):
        """Append to the end of the chain a letter

        :param letter: Letter object
        :return: the current instance
        """
        if not isinstance(letter, Letter):
            raise ValueError("Only letters can be added to a LetterChain, "
                             "received {0}".format(letter))
        self.chain.append(letter)
        return self

    # TODO: remove by distinguishing between different letter objects with same letter text
    def remove(self, letter):
        pass

    def is_valid(self):
        """Check if the chain is ordered alphabetically and has no gaps

        :return: True if valid, False otherwise
        """
        if not self.chain or len(self.chain) == 1:
            return True
        chain = self.chain[:]
        chain.sort()
        if any(x for x, y in collections.Counter(chain).items() if y > 1):
            return False
        next_letters = chain[0].get_next_letters(len(chain)-1)
        next_letters.insert(0, chain[0])
        if chain == next_letters:
            return True
        else:
            return False


class LetterBoard(object):
    """Represents all available letters on the board
    """
    def __init__(self, letters=[]):
        """LetterBoard class initializer

        :param letters: iterable data structure (i.e. list, set) of Letter objects
        """
        self.letters = set(letters)

    def setup(self, n):
        """Initializes the board with n random letters with a precomputed consecutive
        pair of letters

        :param n: int number of letters to initilialize the board with
        :return: the current instance
        """
        if n < 3:
            raise ValueError("The number of letters to initialize the board with "
                             "must be a positive number bigger or equal to 3, "
                             "got <{0}>".format(n))
        self.letters.clear()
        for i in xrange(n-1):
            letter = Letter(random.choice(ALPHABET))
            self.letters.add(letter)
        chosen_letter = random.choice(list(self.letters))
        self.letters.add(chosen_letter.any_adjacent)
        return self

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

    def add_random_letters(self, level):
        """Add some "random" letters according to the level

        :param level: int user game level
        :return: the current instance
        """
        if level < 0:
            raise ValueError("The user level must be at least 1, received <{0}>".format(level))

        if self.find_consecutive_combinations(level+1):
            for _ in xrange(level+1):
                letter = Letter(random.choice(ALPHABET))
                self.letters.add(letter)
        else:
            chosen_letter = random.choice(list(self.letters))
            letters = chosen_letter.get_adjacent_letters(level+1)
            self.letters.update(set(letters))
            letter = Letter(random.choice(ALPHABET))
            self.letters.add(letter)
        return self

    def find_consecutive_combinations(self, n):
        """Find n number of consecutive letters on the board
        For instance, 3 consecutive letters are 'X', 'Y' and 'Z'.

        :param n: int number of consecutive letters to be found on the board
        :return: list of non-duplicate lists with consecutive ordered letter strings
        """
        if n < 2:
            raise ValueError("The minimum number of letters to build a chain is 2, \
                             received <{0}>".format(n))

        adjacent_combinations = []
        text_letters = {l.letter for l in self.letters}
        letters = list(self.letters)
        letters.sort()
        letters = [i for i, _ in itertools.groupby(letters)]
        for letter in letters:
            next_letters = letter.get_next_letters(n-1)
            if next_letters:
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


def is_valid_gap(mask, gap):
    """Check if it's a valid mask considering the gap

    :param gap: int total gap between letters
    :return: True if valid, False otherwise
    """
    if gap < 0:
        raise ValueError("The gap must a be positive int, received <{0}>".format(gap))
    if not mask[0] or not mask[-1]:
        return False
    if gap > len(mask)-2:
        return False

    false_count = mask.count(False)
    if false_count <= gap :
        return True
    else:
        return False
