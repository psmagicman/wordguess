#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from etc.config import db_dir, db_file, word_list
from wordguess.common.connector import init_words_table, init_scoreboard_table

def initialize_db():
    if os.path.exists(db_file):
        return
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    print('creating words')
    init_words_table(word_list)
    print('creating scoreboard')
    init_scoreboard_table()
