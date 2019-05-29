#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import base64

from cryptography.fernet import Fernet, InvalidToken

from etc.config import game_key
from hangman.common.exceptions import TokenError

alphabet_pattern = re.compile('^[a-zA-Z0-9]+$')
DELIM = '|'

def is_letter(ch):
    return bool(alphabet_pattern.match(ch))

def encode_message(message):
    f = Fernet(game_key)
    token = f.encrypt(message.encode())
    return base64.urlsafe_b64encode(token)

def decode_token(token):
    try:
        f = Fernet(game_key)
        return f.decrypt(base64.b64decode(token)).decode('utf-8')
    except InvalidToken as e:
        raise TokenError(token, 'Invalid token given. Please restart game.')

def create_message(*args):
    message = ''
    for arg in args:
        if not message:
            message += str(arg)
        else:
            message += DELIM + str(arg)
    return message
