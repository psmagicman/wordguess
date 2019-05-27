#! /usr/bin/env python3
# -*- coding: utf-8 -*-

class Game(object):
    """docstring for Game"""
    def __init__(self, word, life=None):
        super(Game, self).__init__()
        self.word = word
        self.life = 5 if life is None else life

    def decrement_life(self):
        self.life -= 1

    def get_character_indicies(self, ch):
        return [i for i, val in enumerate(self.word) if val == ch]

    def is_word_finished(self, spaces):
        return ''.join(spaces) == self.word

    def is_in_word(self, letter):
        return letter in self.word
