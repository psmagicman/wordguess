#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import base64

from cryptography.fernet import Fernet

from etc.config import game_key

alphabet_pattern = re.compile('^[a-zA-Z0-9]+$')
DELIM = '_'

def is_letter(ch):
    return bool(alphabet_pattern.match(ch))

def encode_word(word, life):
    f = Fernet(game_key)
    # no cheating by changing life
    concat_word = word + DELIM + str(life)
    token = f.encrypt(concat_word.encode())
    return base64.urlsafe_b64encode(token)

def decode_token(token):
    f = Fernet(game_key)
    return f.decrypt(base64.b64decode(token)).decode('utf-8')