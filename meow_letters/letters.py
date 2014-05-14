import random
import itertools
import collections

from constants.alphabets import ENGLISH_ALPHABET as ALPHABET


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

    @property
    def length(self):
        """Return the length of the chain

        :return: int length of the chain
        """
        return len(self.chain)

    @property
    def empty(self):
        """Check if the chain is empty

        :return: True if chain is empty, False otherwise
        """
        return True if not self.chain else False

    @property
    def last(self):
        """Get the last element from the chain

        :return: the last element from the chain, None if chain is empty
        """
        if self.empty:
            return None
        else:
            return self.chain[-1]

    def add(self, letter):
        """Append to the end of the chain a letter

        :param letter: Letter object
        :return: the current instance
        """
        if not isinstance(letter, Letter):
            raise ValueError("Only letters can be added to a LetterChain, "
                             "received {0}".format(letter))
        letter.select()
        self.chain.append(letter)
        return self

    def remove(self, letter):
        """Remove letter from the chain. All consecutive following letter will be
        removed from the chain too.

        :param letter: Letter object
        :return: the current instance
        """
        if len(self.chain) == 0:
            raise ValueError("Can't remove from empty chain")
        if letter not in self.chain:
            raise ValueError("Error: {0} is not in the chain".format(letter))

        letter_index = self.chain.index(letter)
        for i in reversed(xrange(letter_index, len(self.chain))):
            self.chain[i].unselect()
            self.chain.remove(self.chain[i])
        return self

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
        if self.chain == next_letters:
            return True
        else:
            return False

    def clear(self):
        """Unselect all letters and clear the chain.
        """
        for letter in self.chain:
            letter.unselect()
        self.chain = []


class LetterGrid(object):
    def __init__(self, size):
        self.end = False
        self.size = size
        self.create_grid()
        self.chain = LetterChain()

    def __getitem__(self, item):
        return self.grid[item]

    def create_grid(self):
        """Initializes the grid with None values
        """
        self.grid = [[None for i in range(self.size)] for j in range(self.size)]

    def setup(self, n):
        """Initializes the board with n random letters with a precomputed
        consecutive pair of letters

        :param n: int number of letters to initialize the board with
        :return: the current instance
        """
        self.create_grid()
        random_letters = []
        for i in xrange(n-1):
            letter = Letter(random.choice(ALPHABET))
            random_letters.append(letter)
        chosen_letter = random.choice(random_letters)
        random_letters.append(chosen_letter.any_adjacent)
        self.place_randomly(random_letters)
        return self

    def place_randomly(self, letters):
        """Place randomly on the board a list of letters

        :param letters: iterable data structure of Letter objects
        """
        free_cells = []
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.grid[i][j] is None:
                    free_cells.append([i, j])

        for letter in letters:
            if not free_cells:
                self.end = True
                return
            random.shuffle(free_cells)
            i, j = free_cells.pop()
            self.grid[i][j] = letter

    def iterate(self):
        """Helper iterator. Iterates through all cells.
        """
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_empty(self):
        """Helper iterator. Iterates through empty cells.
        """
        for ix, iy in self.iterate_pos():
            child = self.grid[ix][iy]
            if not child:
                yield ix, iy

    def iterate_pos(self):
        """Helper iterator. Returns index iterator.
        """
        for ix in range(self.size):
            for iy in range(self.size):
                yield ix, iy

    def cycle_end(self, level):
        valid_chain = True
        if self.chain.chain.__len__() == 1:
            valid_chain = False

        for x, y, letter in self.iterate():
            letter.unselect()
            if letter in self.chain.chain:
                if valid_chain:
                    self.grid[x][y] = None
                self.chain.chain.remove(letter)
        self.add_random_letters(level)

    def add_random_letters(self, level):
        """Add some "random" letters according to the level

        :param level: int user game level
        :return: set of new random letters added to the board
        """
        if level < 0:
            raise ValueError("The user level must be at least 1, received <{0}>".format(level))

        random_letters = list()
        letters_qtty = (level + 1) / 2 + 1

        if self.find_consecutive_combinations(letters_qtty):
            for _ in xrange(letters_qtty):
                letter = Letter(random.choice(ALPHABET))
                random_letters.append(letter)
        else:
            chosen_letter = self.random_choice()
            letters = chosen_letter.get_adjacent_letters(letters_qtty)
            letters.remove(chosen_letter)
            random_letters += list(letters)
            letter = Letter(random.choice(ALPHABET))
            random_letters.append(letter)
        self.place_randomly(random_letters)
        return random_letters

    def random_choice(self):
        """Choses a random letter from the board.
        :return: a single Letter object.
        """
        letters_pos = []
        for x, y, letter in self.iterate():
            letters_pos.append([x, y])

        if not letters_pos:
            return None
        else:
            x, y = random.choice(letters_pos)
            return self.grid[x][y]

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
        text_letters = {l.letter for x, y, l in self.iterate()}
        letters = [l for x, y, l in self.iterate()]
        if not letters:
            return True
        letters.sort()
        letters = [i for i, _ in itertools.groupby(letters)]  # de-duplicator
        for letter in letters:
            next_letters = letter.get_next_letters(n-1)
            if next_letters:
                if all(l.letter in text_letters for l in next_letters):
                    combination = [letter.letter] + [i.letter for i in next_letters]
                    adjacent_combinations.extend([combination])

        return adjacent_combinations

    def has_letter(self, letter):
        """Check if the grid contains a specific letter

        :param letter: Letter object
        :return: True if letter is found in the grid, False otherwise
        """
        for ix, iy, child in self.iterate():
            if letter == child:
                return True
        return False

    def is_complete_chain(self):
        """Check if the chain is complete, in other words there are no more other
        consecutive letters in the grid

        :return: True if chain is complete, False - otherwise
        """
        if self.chain.length < 2:
            return False
        last = self.chain.last
        if last:
            next = last.next
            if next:
                return not self.has_letter(next)
            else:
                return True
        else:
            return False
