#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from wordguess.common.connector import initialize_db, get_word_list
from wordguess.common.utils import is_letter
from wordguess.game.game import Game
from wordguess.game.scoreboard import Scoreboard
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
            print('You have entered <%s>, please try again.' % user_input)

def win_screen(score):
    name = input('Congratulations, you won! Please enter your name: ')
    sb = Scoreboard(name, score)
    print('%s, your score is [%s]' % (sb.name, sb.score))
    # sb.save_to_fs()
    sb.save_to_db()

def run():
    initialize_db()
    print('Welcome to Hangman v1.1')
    word_list = get_word_list()
    game = Game(random.choice(word_list))
    word_length = len(game.word)
    spaces = ['_' for i in game.word]
    guess_list = []
    print('Your word has %s characters. %s' % (word_length, '_'*word_length))
    while game.life > 0 and not game.is_word_finished(spaces):
        character = prompt_letter(guess_list)
        guess_list.append(character)
        if game.is_in_word(character):
            indicies = game.get_character_indicies(character)
            for i in indicies:
                spaces[i] = game.word[i]
        else:
            game.decrement_life()
            print('You have %s incorrect guesses remaining.' % game.life)
        print('Letters guessed: %s' % str(guess_list))
        print('Word: ===== %s =====' % ''.join(spaces))

    if game.life > 0 and game.is_word_finished(spaces):
        win_screen(game.life)
    else:
        print('You made too many incorrect guesses.')
    print('Game over.\n')
