#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3

from etc.config import db_dir, db_file, word_list

def initialize_db():
    if os.path.exists(db_file):
        return
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    print('creating words')
    init_words_table(word_list)
    print('creating scoreboard')
    init_scoreboard_table()

def init_words_table(word_list):
    conn = sqlite3.connect(db_file)
    try:
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS words')
        conn.commit()
        c.execute('CREATE TABLE IF NOT EXISTS words (word TEXT NOT NULL)')
        for word in word_list:
            c.execute('INSERT INTO words VALUES (?)', (word,))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.close()

def init_scoreboard_table():
    conn = sqlite3.connect(db_file)
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scores
                    (name TEXT NOT NULL,
                    score INTEGER NOT NULL)''')
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_word_list():
    conn = sqlite3.connect(db_file)
    try:
        word_list = []
        c = conn.cursor()
        c.execute('SELECT word FROM words')
        rows = c.fetchall()
        for row in rows:
            # print(row)
            word_list.append(row[0])
        return word_list
    except Exception as e:
        raise e
    finally:
        conn.close()

def insert_into_scoreboard(name, score):
    conn = sqlite3.connect(db_file)
    # print('inserting into scoreboard')
    try:
        c = conn.cursor()
        c.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.close()
