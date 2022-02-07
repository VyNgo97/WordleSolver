from collections import Counter
import logging
import random
from time import sleep

def read_input_text():
    with open("data/words.txt") as file:
        words = [line.rstrip() for line in file]
    return words

# returns a counter object of letters and their frequency
def letter_frequency(word_list):
    frequency = Counter()
    letters = word_list
    for word in letters:
        for letter in word:
            frequency[letter]+=1
    return frequency

# tried calculating weights each iteratio but as the list gets smaller, the weights don't tell as much
def calculate_weight(word_list, correct_letters):
    weights_dict = letter_frequency(read_input_text())
    vowels = ['a', 'e', 'i', 'o', 'u']
    for letter in correct_letters:
        if letter in vowels:
            weights_dict[letter] = 1
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

scores = {}

def main(winning_word):
    guess_counter = 1
    guess = 'later'
    input_list = read_input_text()
    # winning_word = random.choice(input_list)
    # winning_word = 'soggy'
    used_letters = set()
    while(True):
        logging.info('try number: %d and guess is: %s', guess_counter, guess)
        logging.info('word is: %s', winning_word)
        if(guess == winning_word):
            # checking results
            if guess_counter in scores:
                scores[guess_counter] += 1
            else:
                scores[guess_counter] = 1
            logging.info('you win!')
            break
        if(guess_counter == 1):
            green_letters = [guess[i] for i in range(len(guess)) if guess[i] == winning_word[i]]
            yellow_letters = [letter for letter in guess if letter in winning_word and letter not in green_letters]
            correct_letters = green_letters + yellow_letters
            used_letters = set(guess) - set(green_letters).union(set(yellow_letters))
            indices_green = [i for i in range(len(guess)) if guess[i] == winning_word[i]]
            indices_yellow = [i for i in range(len(guess)) if guess[i] in winning_word and guess[i] != winning_word[i]]
            if(len(green_letters) == 0): 
                updated_words_list = [y for y in input_list if all(x not in y for x in used_letters)]
            else:
                updated_words_list = [y for y in input_list if all(x in y for x in green_letters)]
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
        else:
            # remove guess from list and reassess correct letters (add them to correct_letters if not in their already)
            for i in range(len(guess)):
                if guess[i] not in green_letters and guess[i] in winning_word:
                    if guess[i] == winning_word[i]:
                        green_letters.append(guess[i])
                        indices_green.append(i)
                    elif guess[i] not in yellow_letters:
                        yellow_letters.append(guess[i])
                        indices_yellow.append(i)
                elif guess[i] not in winning_word:
                    used_letters.add(guess[i])

            logging.info("letters not in word: %s", used_letters)
            
            updated_words_list.remove(guess)
            if(len(green_letters) == 0 and len(yellow_letters) == 0):
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
            elif(len(green_letters) == 0):
                updated_words_list = [y for y in updated_words_list if all(x in y for x in yellow_letters)]
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
            elif(len(yellow_letters) == 0):
                updated_words_list = [y for y in updated_words_list if all(x in y for x in green_letters)]
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]
            else:
                updated_words_list = [y for y in updated_words_list if all(x in y for x in correct_letters)]
                updated_words_list = [y for y in updated_words_list if all(x not in y for x in used_letters)]

        logging.info('green letters: %s', str(green_letters))
        logging.info('green indices: %s', str(indices_green))
        logging.info('yellow letters: %s', str(yellow_letters))
        logging.info('yellow indices: %s', str(indices_yellow))
        logging.info('correct letters so far: %s', str(correct_letters))
        guess_counter+=1
        # filter possible answers by letters in correct_letters
        # all() checks if all the items in a list are true- here (x in y) returns a boolean we add to a list which gets assessed by all()
        # improve this part for better performance- maybe decrease list size based on closer_match as well?

        #craft new list which only words where the matching letters are at the correct index
        # closer_match = [x for x in updated_words_list if all(x for i in indices if x[i] == correct_letters[])]
        # also add in yellow letters
        # print(sorted(zip(indices, green_letters))) <- you can sort a zipped list the order of the zip matters here
        updated_words_list = [y for y in updated_words_list if all(y[i] == j for i,j in sorted(zip(indices_green, green_letters)))]
        updated_words_list = [y for y in updated_words_list if all(y[i] != j for i,j in sorted(zip(indices_yellow, yellow_letters)))]
        # updated_words_list = [x for x in updated_words_list if all(y in x for y in yellow_letters)]
        logging.info('length of list: %d', len(updated_words_list))
        logging.info('updated words list: %s', updated_words_list)

        if(len(correct_letters) < 3):
            logging.info("search mode")
            # guess should be with letters that are not in the temp_list but still using weights
            # take updated list, for each element subtract correct letters .replace() and calculate max, filter list
            search_list = []
            if(len(correct_letters) > 0):
                for word in updated_words_list:
                    for letter in correct_letters:
                        temp = word.replace(letter, '')
                    if len(temp) >= 5-len(correct_letters):
                        search_list.append(word)
            
            logging.info("search mode list: %s", search_list)
            # search_list = [x for x in updated_words_list if all(y not in x for y in correct_letters)]
            if(len(search_list) != 0):
                guess = calculate_weight(search_list, correct_letters)
            else:
                guess = calculate_weight(updated_words_list, correct_letters)
        #guess should determined using weight of each letter
        #TODO update weight based on how many vowels we have guessed and don't allow repeated characters on the first pass
        else:
            logging.info("heuristics mode")
            guess = calculate_weight(updated_words_list, correct_letters)

        logging.info('========================================================================')
        # sleep(.5)

if __name__ == '__main__':
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    for word in read_input_text():
        main(word)
    print(scores)