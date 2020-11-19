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


class Person:
    def __init__(self, id_artist, name, date_of_birth, date_of_death):
        self.id_artist = id_artist
        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death

    def __str__(self):
        id_artist = self.id_artist
        name = self.name
        date_of_birth = self.date_of_birth
        date_of_death = self.date_of_death
        if id_artist is None:
            id_artist = 'None'
        if name is None:
            name = 'None'
        if date_of_birth is None:
            date_of_birth = 'None'
        if date_of_death is None:
            date_of_death = 'None'

        return 'id: ' + id_artist + '; name: ' + name + '; date_of_birth: ' + date_of_birth + '; date_of_death: ' + date_of_death


def get_id_from_line(line):
    pattern_id = '<http://rdf.freebase.com/ns/g.(.+?)>'
    result_id = re.search(pattern_id, line)
    if result_id:
        id_art = result_id.group(1)
        return id_art
    return 'Not Found'


def fix_date(date):
    if len(date) == 4:
        date = date + '-01-01'
    return date


def get_attribute_by_id(file_line, id_artist):
    id_pattern = '(g.' + id_artist + ')>'
    m = re.search(id_pattern, file_line)
    if m:
        found = m.group(1)
        if found == 'g.' + id_artist:
            n = re.search('"(.+?)"', file_line)
            if n:
                found1 = n.group(0)
                found1 = re.sub('["]', '', found1)
                return found1
    return 'Not Found'


def get_attribute_from_line(file_line):
    n = re.search('"(.+?)"', file_line)
    if n:
        found1 = n.group(0)
        found1 = re.sub('["]', '', found1)
        return found1
    return 'Not Found'


def check_if_string_in_file(read_obj, string_to_search):
    read_obj.seek(0, 0)
    for my_line in read_obj:
        if string_to_search in my_line:
            read_obj.seek(2)
            return True
    return False


for line in sys.stdin:
    str_line = str(line)
    artist_id = get_id_from_line(str_line).strip()
    if artist_id in artists:
        if artist_id != 'Not Found':
            pattern_name = '<http://rdf.freebase.com/ns/type.object.name>'
            result_name = re.search(pattern_name, str_line)
            if result_name:
                p = Person(artist_id, get_attribute_from_line(str_line), None, None)
                print(p)
            pattern_date_of_birth = '<http://rdf.freebase.com/ns/people.person.date_of_birth>'
            result_date_of_birth = re.search(pattern_date_of_birth, str_line)
            if result_date_of_birth:
                p = Person(artist_id, None, fix_date(get_attribute_from_line(str_line)), None)
                print(p)
            pattern_date_of_death = '<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>'
            result_date_of_death = re.search(pattern_date_of_death, str_line)
            if result_date_of_death:
                p = Person(artist_id, None, None, fix_date(get_attribute_from_line(str_line)))
                print(p)
