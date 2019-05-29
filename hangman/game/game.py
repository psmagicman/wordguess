#! /usr/bin/env python3
# -*- coding: utf-8 -*-

def get_character_indicies(word, ch):
    return [i for i, val in enumerate(word) if val == ch]

def is_word_finished(word, spaces):
    return ''.join(spaces) == word
