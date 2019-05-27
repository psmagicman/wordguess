#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re

alphabet_pattern = re.compile('^[a-zA-Z0-9]+$')

def is_letter(ch):
    return bool(alphabet_pattern.match(ch))