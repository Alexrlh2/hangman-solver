import guesser
import file_reader
import timeit

WORD_FILE = 'words.txt'

def give_feedback(guesser, guess, solution_word):
    """takes a guesser object, a guess, and a solution word. Checks the guess and updates the guesser object's knowledge"""
    if len(solution_word) != len(guesser.known_letters):
        raise ValueError('Attempting to give feedback for wrong length word')

    if guess in solution_word:
        for i, letter in enumerate(solution_word):
            if guess == letter:
                guesser.known_letters[i] = guess
    else:
        guesser.known_nonletters.add(guess)
        guesser.incorrect_guess_counter += 1


def menu_choice():
    """gives the user options and returns the result"""
    print('Welcome to hangman solver!\n')
    print('1:   User-mode - \t enter a word for it to be guessed. See status updates in real time.')
    print(
        "2:   Random-mode - \t see guesser's performance against n randomly selected english words. See summary of performance.")
    return int(input('Enter a number to select a mode:'))


def new_round(guesser, solution_word, silent_mode=False):
    """takes a guesser object, and a word. Gets and checks guesses from the guesser until complete. In silent mode
    no status updates are given. Returns the number of guesses taken. If valid words are loaded into memory to increase
    performance, they can be passed as list_of_words"""
    while ''.join(guesser.known_letters) != solution_word:
        if not guesser.unguessed_letters:
            raise LookupError('Word not found')
        guess = guesser.produce_guess()
        give_feedback(guesser, guess, solution_word)
        guesser.update_possible_words()
        if not silent_mode:
            print(f'Next guess is {guess}')
            guesser.disaplay_status()
            print()
    if not silent_mode:
        print(f'The word was {solution_word}. The guesser made {guesser.incorrect_guess_counter} incorrect guesses')
    return guesser.incorrect_guess_counter


def run_user_mode():
    """runs a guessing round with user input and status updates"""
    solution_word = input('Enter an english word (excluding acronyms, abbreviations, and proper nouns):').upper()
    new_round(guesser.Guesser(len(solution_word)), solution_word)


def run_random_mode():
    """runs a game in random-mode, playing n guessing rounds with randomly selected words. Summary of performance"""
    n = int(input('How many words should be guessed?:'))
    if input('Enter Y to preload valid words into memory. This will increase speed but use more memory: ') == 'Y':
        use_memory = True
        all_english_words = file_reader.get_all_words(WORD_FILE)
    else:
        use_memory = False
    word_lengths = []
    guessed_words = {}
    words = file_reader.get_n_random_words(WORD_FILE, n)
    print('Solving puzzles')
    tic = timeit.default_timer()
    for word in words:
        if use_memory:
            wrong_guesses = (new_round(guesser.Guesser(len(word), all_english_words), word, True))
        else:
            wrong_guesses = (new_round(guesser.Guesser(len(word)), word, True))
        guessed_words.update({word: wrong_guesses})
        word_lengths.append(len(word))
    toc = timeit.default_timer()
    print(
        f'Completed {n} puzzles in {toc - tic} seconds. The average word length was {sum(word_lengths) / n} letters, and the average number of incorrect guesses '
        f'was {sum(guessed_words.values()) / n}')
    if input('Enter Y to see list of guessed words and number of incorrect guesses: ') == 'Y':
        for w in guessed_words:
            print(f'{w} took {guessed_words[w]} incorrect guesses')


def main():
    mode = menu_choice()
    if mode == 1:
        run_user_mode()
    elif mode == 2:
        run_random_mode()


if __name__ == '__main__':
    main()
