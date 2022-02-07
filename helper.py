from collections import Counter
import logging
import random
from time import sleep
from turtle import update

def read_input_text():
    with open("data/words.txt") as file:
        words = [line.rstrip() for line in file]
    # logging.info("words list length: %d", len(words))
    return words

# returns a counter object of letters and their frequency
def letter_frequency():
    frequency = Counter()
    letters = read_input_text()
    for word in letters:
        for letter in word:
            frequency[letter]+=1
    return frequency

def calculate_weight(word_list):
    weights_dict = {'e': 1233, 'a': 979, 'r': 899, 'o': 754, 't': 729, 'l': 719, 'i': 671, 's': 669, 'n': 575, 'c': 477, 'u': 467, 'y': 425, 'd': 393, 'h': 389, 'p': 367, 'm': 316, 'g': 311, 'b': 281, 'f': 230, 'k': 210, 'w': 195, 'v': 153, 'z': 40, 'x': 37, 'q': 29, 'j': 27}
    weighted_word = ''
    curr_weight = 0
    max_weight = 0
    for word in word_list:
        for letter in word:
            curr_weight+=weights_dict[letter]
        if curr_weight > max_weight:
            max_weight = curr_weight
            weighted_word = word
        curr_weight = 0
    logging.info('greatest weighted word is %s with weight %d', weighted_word, max_weight)
    return weighted_word

def main():
    guess_counter = 1
    input_list = read_input_text()
    # data = ["", "", "", "", ""]
    used_letters = set()
    guess = input('guess: ')
    while(True):
        if(guess_counter == 1):
            correct_letters = list(input('correct letters: '))
            used_letters = set(guess) - set(correct_letters)
            logging.info(used_letters)
            indices = list(input('their indices: '))
            if(len(correct_letters) == 0):
                updated_words_list = [y for y in input_list if all(x not in y for x in used_letters)]
            else:
                updated_words_list = [y for y in input_list if all(x in y for x in correct_letters)]
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
        else:
            # remove guess from list and reassess correct letters (add them to correct_letters if not in their already)
            correct_letters = list(input('correct letters: '))
            for letter in guess:
                if letter not in correct_letters:
                    used_letters.add(letter)
            
            indices = list(input('indices: '))
            updated_words_list.remove(guess)
            updated_words_list = [y for y in updated_words_list if all(x in y for x in correct_letters)]
            # clean up by making one comprehension?
            updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
            print(updated_words_list)


        guess_counter+=1
        if(len(correct_letters) < 3):
            logging.info("search mode")
            # temp_list = [y for y in updated_words_list if all(x not in y for x in correct_letters)]
            # guess should be with letters that are not in the temp_list but still using weights
            suggestion = calculate_weight(updated_words_list)
            guess = input('guess again: ')
        else:
            logging.info("heuristics mode")
            #craft new list which only words where the matching letters are at the correct index
            # closer_match = [x for x in updated_words_list if all(x for i in indices if x[i] == correct_letters[])]
            closer_match = [y for y in updated_words_list if all(y.index(i) == j for i,j in zip(correct_letters, indices))]
            #guess should determined using weight of each letter
            guess = calculate_weight(closer_match)

if __name__ == '__main__':
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    main()