#!/usr/bin/env python
"""mapper.py"""
import re
import sys

file_name = 'input2.txt'
f_artist = open(file_name, 'r')
artists = set()
for a in f_artist:
    if a not in artists:
        artists.add(a.strip())


def get_id_from_line(line):
    pattern_id = '<http://rdf.freebase.com/ns/(.+?)>'
    result_id = re.search(pattern_id, line)
    if result_id:
        id_art = result_id.group(1)
        return id_art
    return 'Not Found'


def fix_date(date):
    if len(date) == 4:
        date = date + '-01-01'
    return date


def get_attribute_from_line(file_line):
    n = re.search('"(.+?)"', file_line)
    if n:
        found1 = n.group(0)
        found1 = re.sub('["]', '', found1)
        return found1
    return 'Not Found'


def get_name_from_line(file_line):
    n = re.search('"(.+?)"@en', file_line)
    if n:
        found1 = n.group(1)
        return found1
    return 'None'


for line in sys.stdin:
    str_line = str(line)
    artist_id = get_id_from_line(str_line).strip()
    if artist_id in artists:
        pattern_date_of_birth = '<http://rdf.freebase.com/ns/people.person.date_of_birth>'
        result_date_of_birth = re.search(pattern_date_of_birth, str_line)
        if result_date_of_birth:
            print('id: ' + artist_id + '; name: None' + '; date_of_birth: ' + fix_date(get_attribute_from_line(str_line)) + '; date_of_death: None')
        pattern_date_of_death = '<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>'
        result_date_of_death = re.search(pattern_date_of_death, str_line)
        if result_date_of_death:
            print('id: ' + artist_id + '; name: None' + '; date_of_birth: None' + '; date_of_death: ' + fix_date(get_attribute_from_line(str_line)))
        pattern_name = '<http://rdf.freebase.com/ns/type.object.name>'
        result_name = re.search(pattern_name, str_line)
        if result_name:
            print('id: ' + artist_id + '; name: ' + get_name_from_line(str_line) + '; date_of_birth: None' + '; date_of_death: None')
