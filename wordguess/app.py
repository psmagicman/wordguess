#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import re

from wordguess.game.game import Game
from wordguess.game.scoreboard import Scoreboard
from etc.config import word_list

"""main driver for the game to run on command line"""
alphabet_pattern = re.compile('^[a-zA-Z0-9]+$')
is_letter = lambda x: bool(alphabet_pattern.match(x))

def init():
    # if db file doesn't exist, create it
    pass

def prompt_letter(guess_list):
    while True:
        user_input = raw_input('Please enter a single alphanumeric character (case insensitive): ')
        if user_input.lower() in guess_list:
            print 'You already entered this letter, please try again.'
        elif len(user_input) == 1 and is_letter(user_input):
            return user_input.lower()
        else:
            print 'You have entered <%s>, please try again.' % user_input

def win_screen(score):
    name = raw_input('Congratulations, you won! Please enter your name: ')
    sb = Scoreboard(name, score)
    print '%s, your score is [%s]' % (sb.name, sb.score)
    sb.save_to_fs()

def run():
    init()
    print 'Welcome to Hangman v1.0'
    game = Game(word_list)
    word_length = len(game.word)
    print 'Your word has %s characters. %s' % (word_length, '_'*word_length)
    while game.life > 0 and not game.is_word_finished():
        letter = prompt_letter(game.guess_list)
        game.guess_list.append(letter)
        if game.is_in_word(letter):
            indicies = game.get_character_indicies(letter)
            for i in indicies:
                game.update_space_index(i)
        else:
            game.decrement_life()
            print 'You have %s incorrect guesses remaining.' % game.life
        print 'Letters guessed: %s' % str(game.guess_list)
        print 'Word: ===== %s =====' % ''.join(game.spaces)

    if game.life > 0 and game.is_word_finished():
        win_screen(game.life)
    else:
        print 'You made too many incorrect guesses.'
    print 'Game over.\n'
