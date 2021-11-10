import file_reader
import string
import math


class Guesser:
    """A class used to create guesser objects which track revealed information about a particular word and produce
    guesses based on this information"""

    def __init__(self, word_length=0, list_of_words=None):
        """If words are loaded into memory to increase performance, they can be passed as list_of_words"""
        if list_of_words:
            self.possible_words = []
            for word in list_of_words:
                if len(word) == word_length:
                    self.possible_words.append(word)
                elif len(word) > word_length:
                    break
        else:
            self.possible_words = file_reader.get_words_by_length('words.txt', word_length)
        self.known_letters = [''] * word_length
        self.incorrect_guess_counter = 0
        self.known_nonletters = set()
        self.unguessed_letters = set(string.ascii_uppercase)

    def produce_guess(self):
        """returns the un-guessed letter which appears in as close to half of possible_words as possible"""
        # add functionality for guessing whole word
        n = len(self.possible_words)
        frequencies = dict.fromkeys(self.unguessed_letters, 0)
        for letter in frequencies:
            for word in self.possible_words:
                if letter in word:
                    frequencies[letter] += 1
        distances_from_half = {letter: abs(math.ceil(n / 2) - count) for (letter, count) in frequencies.items()}
        guess = min(distances_from_half, key=distances_from_half.get)
        self.unguessed_letters.discard(guess)
        return guess

    def update_possible_words(self):
        new_possible_words = []
        for word in self.possible_words:
            valid = True
            for letter in self.known_nonletters:
                if letter in word:
                    valid = False
                    break
            if not valid:
                continue
            for i, letter in enumerate(self.known_letters):
                if letter and letter != word[i]:
                    valid = False
                    break
            if valid:
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def disaplay_status(self):
        print(''.join(['_' if not letter else letter for letter in self.known_letters]))
        print(f'incorrect guesses: {self.incorrect_guess_counter}')
