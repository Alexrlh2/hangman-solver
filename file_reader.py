import random
import linecache

def get_file_length(word_file):
    counter = 0
    with open(word_file) as words:
        for line in words:
            counter +=1
    return counter

def get_words_by_length(word_file, length):
    """returns english words of a given length from a specified file"""

    selected_words = []

    with open(word_file) as english_words:
        for line in english_words:
            word = line.rstrip()
            if len(word) == length:
                selected_words.append(word)
            elif len(word) > length:
                break

    return selected_words


def get_n_random_words(word_file, n):
    file_length = get_file_length(word_file)
    words = []
    for i in range(n):
        line_num = random.randrange(0, file_length)
        words.append(linecache.getline(word_file, line_num).rstrip())
    return words


def get_all_words(word_file):
    words = []
    with open(word_file) as english_words:
        for line in english_words:
            words.append(line.rstrip())
    return words




