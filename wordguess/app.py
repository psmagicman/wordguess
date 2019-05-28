#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from wordguess.common.connector import get_word_list, db_file_exists
from wordguess.common.utils import is_letter
from wordguess.common.exceptions import DbError
import wordguess.game.game as game
import wordguess.game.scoreboard as scoreboard
from etc.config import word_list, db_file

"""main driver for the game to run on command line"""

def prompt_letter(guess_list):
    while True:
        user_input = input('Please enter a single alphanumeric character (case insensitive): ')
        if user_input.lower() in guess_list:
            print('You already entered this letter, please try again.')
        elif len(user_input) == 1 and is_letter(user_input):
            return user_input.lower()
        else:
            print('You have entered invalid char <%s>, please try again.' % user_input)

def win_screen(score):
    name = input('Congratulations, you won! Please enter your name: ')
    print('%s, your score is [%s]' % (name, score))
    try:
        scoreboard.save_to_db(name, score)
    except DbError as e:
        print(e.message, e.values)
    

def initialize_game(word_list):
    word = random.choice(word_list)
    return {
        'word': word,
        'life': 5,
        'spaces': ['_' for i in word],
        'guesses': []
    }

def run():
    if not db_file_exists():
        print("No db file found, please set it up and try again.")
        exit(1)
    print('Welcome to Hangman v1.2')
    word_list = get_word_list()
    data = initialize_game(word_list)
    word_length = len(data['word'])
    print('Your word has %s characters. %s' % (word_length, '_'*word_length))
    while data['life'] > 0 and not game.is_word_finished(data['word'], data['spaces']):
        character = prompt_letter(data['guesses'])
        data['guesses'].append(character)
        if character in data['word']:
            indicies = game.get_character_indicies(data['word'], character)
            for i in indicies:
                data['spaces'][i] = data['word'][i]
        else:
            data['life'] -= 1
            print('You have %s incorrect guesses remaining.' % data['life'])
        print('Letters guessed: %s' % str(data['guesses']))
        print('Word: ===== %s =====' % ''.join(data['spaces']))

    if data['life'] > 0 and game.is_word_finished(data['word'], data['spaces']):
        win_screen(data['life'])
    else:
        print('You made too many incorrect guesses.')
    print('Game over.\n')
