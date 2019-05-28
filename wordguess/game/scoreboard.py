#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv

from etc.config import score_directory, score_file
from wordguess.common.connector import insert_into_scoreboard
from wordguess.common.exceptions import DbError

def save_to_fs(name, score):
    final_score = [name, score]
    if not os.path.exists(score_directory):
        os.makedirs(score_directory)
    filepath = os.path.join(score_directory, score_file)
    with open(filepath, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(final_score)

def save_to_db(name, score):
    try:
        insert_into_scoreboard(name, score)
    except DbError as e:
        raise e
    
