#!/usr/bin/env python
"""reducer.py"""
import sys

before_id = ''

# input comes from STDIN
for line in sys.stdin:
    if line != before_id:
        before_id = line
        print(line[:len(line) - 1])
