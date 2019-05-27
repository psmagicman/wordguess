#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv

from etc.config import score_directory, score_file
from wordguess.common.connector import insert_into_scoreboard

class Scoreboard(object):
    """docstring for Scoreboard"""
    def __init__(self, name, score):
        super(Scoreboard, self).__init__()
        self.name = name
        self.score = score
    
    def save_to_fs(self):
        final_score = [self.name, self.score]
        if not os.path.exists(score_directory):
            os.makedirs(score_directory)
        filepath = os.path.join(score_directory, score_file)
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(final_score)

    def save_to_db(self):
        insert_into_scoreboard(self.name, self.score)
