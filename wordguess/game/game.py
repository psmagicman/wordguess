#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

class Game(object):
    """docstring for Game"""
    def __init__(self, word_list):
        super(Game, self).__init__()
        self.word = random.choice(word_list)
        self.spaces = ['_' for i in self.word]
        self.life = 5
        self.guess_list = []

    def decrement_life(self):
        self.life -= 1

    def get_character_indicies(self, ch):
        return [i for i, val in enumerate(self.word) if val == ch]

    def update_space_index(self, index):
        self.spaces[index] = self.word[index]

    def is_word_finished(self):
        return ''.join(self.spaces) == self.word

    def is_in_word(self, letter):
        return letter in self.word
