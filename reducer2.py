#!/usr/bin/env python
"""reducer.py"""
import sys

before_id = ''
current_id = ''
artist_id = 'id: None'
name = 'name: None'
date_of_birth = 'date_of_birth: None'
date_of_death = 'date_of_death: None'

# input comes from STDIN
for line in sys.stdin:
    result = line.split("; ")
    current_id = result[0]
    if current_id == before_id:
        if result[0].strip() != 'id: None':
            artist_id = result[0].strip()
        if result[1].strip() != 'name: None':
            name = result[1].strip()
        if result[2].strip() != 'date_of_birth: None':
            date_of_birth = result[2].strip()
        if result[3].strip() != 'date_of_death: None':
            date_of_death = result[3].strip()
    else:
        if artist_id != 'id: None' and name != 'name: None':
            print(artist_id + '; ' + name + '; ' + date_of_birth + '; ' + date_of_death)
        artist_id = result[0].strip()
        name = result[1].strip()
        date_of_birth = result[2].strip()
        date_of_death = result[3].strip()
        before_id = current_id
