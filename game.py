#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import random
import re
import datetime
import csv
import os

word_list = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
alphabet_pattern = re.compile('^[a-zA-Z0-9]+$')
is_letter = lambda x: bool(alphabet_pattern.match(x))
score_directory = 'scoreboard'
score_file = 'scoreboard.csv'

def pick_word(word_list):
    return random.choice(word_list)

def prompt_letter(guess_list):
    while True:
        user_input = raw_input('Please enter a single alphanumeric character (case insensitive): ')
        if user_input.lower() in guess_list:
            print 'You already entered this letter, please try again.'
        elif len(user_input) == 1 and is_letter(user_input):
            return user_input.lower()
        else:
            print 'You have entered <%s>, please try again.' % user_input

def word_finished(spaces, word):
    return ''.join(spaces) == word

def win_statement():
    print 'Congratulations, you won!'
    return raw_input('Please enter your name: ')

def save_score(score, name):
    print '%s, your score is [%s]' % (name, score)
    final_score = [name, score]
    if not os.path.exists(score_directory):
        os.makedirs(score_directory)
    filepath = os.path.join(score_directory, score_file)
    with open(filepath, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(final_score)

def millis_since_epoch(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def get_char_indicies(word, char):
    return [idx for idx, val in enumerate(word) if val == char]

def main():
    print 'Welcome to Hangman v0.1'
    guess_list = []
    life_counter = 5
    word = pick_word(word_list)
    # print word
    spaces = ['_' for i in word]
    word_length = len(word)
    print 'Your word has %s characters. %s' % (word_length, '_'*word_length)
    while life_counter > 0 and not word_finished(spaces, word):
        letter = prompt_letter(guess_list)
        guess_list.append(letter)
        if letter in word:
            # get indices of the letter in the word
            indicies = get_char_indicies(word, letter)
            # replace indicies in spaces
            for index in indicies:
                spaces[index] = word[index]
        else:
            life_counter -= 1
            print 'You have %s incorrect guesses remaining.' % (life_counter)
        print 'Letters guessed: %s ' % str(guess_list)
        print 'Word: === %s ===' % ''.join(spaces)

    if life_counter > 0 and word_finished(spaces, word):
        player_name = win_statement()
        save_score(life_counter, player_name)
    else:
        print 'You made too many incorrect guesses. Game over.'

if __name__ == '__main__':
    main()