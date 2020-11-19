#!/usr/bin/env python
"""reducer.py"""
import sys

before_id = ''
current_id = ''
id = 'id: None'
name = 'name: None'
date_of_birth = 'date_of_birth: None'
date_of_death = 'date_of_death: None'
# input comes from STDIN
for line in sys.stdin:
    # print(line[:len(line) - 1])
    line = line[:len(line) - 1]
    result = line.split("; ")
    current_id = result[0]
    if current_id == before_id:
        if result[0] != 'id: None':
            id = result[0]
        if result[1] != 'name: None':
            name = result[1]
        if result[2] != 'date_of_birth: None':
            date_of_birth = result[2]
        if result[3][:len(result[3]) - 1] != 'date_of_death: None':
            date_of_death = result[3]
    else:
        if id != 'id: None':
            print(id + '; ' + name + '; ' + date_of_birth + '; ' + date_of_death)
        id = 'id: None'
        name = 'name: None'
        date_of_birth = 'date_of_birth: None'
        date_of_death = 'date_of_death: None'
    before_id = current_id
