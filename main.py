import re
import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from const import (
    SAMPLE_DATA_DIR,
    ES_HOST,
    ES_PORT
)


def fix_date(date):
    if len(date) == 4:
        date = date + '-01-01'
    return date


def get_artist_file():
    f = open('milionko.txt', 'r+')
    artists_f = open('final_artist.txt', 'r+')
    for line in f:
        str_line = str(line)
        pattern_artist = '<http://rdf.freebase.com/ns/music.artist>'
        result_artist = re.search(pattern_artist, str_line)
        if result_artist:
            pattern_id = '<http://rdf.freebase.com/ns/(.+?)>'
            result_id = re.search(pattern_id, str_line)
            if result_id:
                artist_id = result_id.group(1)
                artists_f.write(artist_id + '\n')


def get_id_from_line(line):
    pattern_id = '<http://rdf.freebase.com/ns/(.+?)>'
    result_id = re.search(pattern_id, line)
    if result_id:
        id_art = result_id.group(1)
        return id_art
    return 'Not Found'


def get_attribute_from_line(file_line):
    n = re.search('"(.+?)"', file_line)
    if n:
        found1 = n.group(0)
        found1 = re.sub('["]', '', found1)
        return found1
    return 'None'


def get_name_from_line(file_line):
    n = re.search('"(.+?)"@en', file_line)
    if n:
        found1 = n.group(1)
        return found1
    return 'None'


def get_artist_name_dates(artists):
    # freebase-head-10000000.txt
    f = open('milionko.txt', 'r+')
    last_final_f = open('last_final1.txt', 'r+')
    count = 0
    for line in f:
        str_line = str(line)
        artist_id = get_id_from_line(str_line).strip()
        if artist_id in artists:
            pattern_date_of_birth = '<http://rdf.freebase.com/ns/people.person.date_of_birth>'
            result_date_of_birth = re.search(pattern_date_of_birth, str_line)
            if result_date_of_birth:
                last_final_f.write('id: ' + artist_id + '; name: None' + '; date_of_birth: ' + fix_date(get_attribute_from_line(str_line)) + '; date_of_death: None' + '\n')
            pattern_date_of_death = '<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>'
            result_date_of_death = re.search(pattern_date_of_death, str_line)
            if result_date_of_death:
                if fix_date(get_attribute_from_line(str_line)) != 'Not Found':
                    count = count + 1
                    last_final_f.write('id: ' + artist_id + '; name: None' + '; date_of_birth: None' + '; date_of_death: ' + fix_date(get_attribute_from_line(str_line)) + '\n')
            pattern_name = '<http://rdf.freebase.com/ns/type.object.name>'
            result_name = re.search(pattern_name, str_line)
            if result_name:
                last_final_f.write('id: ' + artist_id + '; name: ' + get_name_from_line(str_line) + '; date_of_birth: None' + '; date_of_death: None' + '\n')
    print(count)


def reducer_simulation():
    last_final_f = open('last_final1.txt', 'r+')
    counter = 0
    before_id = ''
    current_id = ''
    id = 'id: None'
    name = 'name: None'
    date_of_birth = 'date_of_birth: None'
    date_of_death = 'date_of_death: None'
    # input comes from STDIN
    for line in last_final_f:
        line = line.strip()
        result = line.split("; ")
        current_id = result[0]
        if current_id == before_id:
            if result[0].strip() != 'id: None':
                id = result[0].strip()
            if result[1].strip() != 'name: None':
                name = result[1].strip()
            if result[2].strip() != 'date_of_birth: None':
                date_of_birth = result[2].strip()
            if result[3].strip() != 'date_of_death: None':
                date_of_death = result[3].strip()
        else:
            if id != 'id: None' and name != 'name: None':
                if date_of_death != 'date_of_death: None':
                    counter = counter + 1
                print(id + '; ' + name + '; ' + date_of_birth + '; ' + date_of_death)
                id = result[0].strip()
                name = result[1].strip()
                date_of_birth = result[2].strip()
                date_of_death = result[3].strip()
            before_id = current_id
    print(counter)


class Artist:
    def __init__(self, id_artist, name, date_of_birth, date_of_death):
        self.id_artist = id_artist
        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death

    def prepare_for_json(self):
        return {
            'id_artist': self.id_artist,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'date_of_death': self.date_of_death
        }


def statistical_analysis(file_name):
    f = open(file_name, 'r')
    count = 0
    empty_names = 0
    empty_births = 0
    empty_deaths = 0
    for line in f:
        parsed_line = line.split("; ")
        artist_id = parsed_line[0][4:]
        artist_name = parsed_line[1][6:]
        artist_birth = parsed_line[2][15:]
        artist_death = parsed_line[3][15:].strip()
        count = count + 1
        if artist_name == 'None':
            empty_names = empty_names + 1
        if artist_birth == 'None':
            empty_births = empty_births + 1
        if artist_death == 'None':
            empty_deaths = empty_deaths + 1

    print('Overall: ' + str(count) + ', empty names: ' + str(empty_names) + ', empty births: ' + str(empty_births) + ', empty deaths: ' + str(empty_deaths))


def parse_output(file_name):
    artists = []
    f = open(file_name, 'r')
    count = 0
    for line in f:
        parsed_line = line.split("; ")
        artist = Artist(parsed_line[0][4:], parsed_line[1][6:], parsed_line[2][15:], parsed_line[3][15:].strip())
        artists.append(artist)
        count = count + 1

    artist_json = json.dumps([artist.prepare_for_json() for artist in artists])
    # print(json.dumps(artist_json, indent=4, sort_keys=True))
    f = open('artists_json.json', 'w')
    f.write(artist_json)
    print(count)
    f.close()


def main_final():
    file_name = 'VINF_final_output/input3.txt'
    parse_output(file_name)
    statistical_analysis(file_name)


def main():
    # get a file which contains only artists
    get_artist_file()
    # get files of names,dates of birth and dates of death

    file_name = 'final_artist.txt'
    f_artist = open(file_name, 'r')
    artists = set()
    for a in f_artist:
        if a not in artists:
            artists.add(a.strip())

    get_artist_name_dates(artists)

    reducer_simulation()


# Part 3 - Elastic Search
def load_data():
    with open(f'artists_json.json') as f:
        data = json.load(f)

    return data


def search_by_name(_index, name):
    es = Elasticsearch(hosts=ES_HOST, port=ES_PORT)
    query_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "name": name
                    }
                }
            }
        }
    }
    # result = es.search(index=_index, body={"query": {"match_all": {}}}, size=100)
    result = es.search(index="artists", body=query_body)
    # print("query hits:", result["hits"]["hits"])
    # print("total hits:", len(result["hits"]["hits"]))
    # print('You searched for: ')
    name = result["hits"]["hits"][0]['_source']['name']
    date_of_birth = result["hits"]["hits"][0]['_source']['date_of_birth']
    date_of_death = result["hits"]["hits"][0]['_source']['date_of_death']
    print('Based on your input, we found the following artist: ')
    print(name + '; date of birth: ' + date_of_birth + '; date of death: ' + date_of_death)
    return result["hits"]["hits"][0]['_source']


def insert_data(data: list, index='artists'):
    bulk_string = ''
    number_of_doc_in_bulk = 0
    for doc in data:
        print(number_of_doc_in_bulk)
        doc_json = doc
        doc_id = doc_json['id_artist']
        # doc_id = re.match('^{"id": "[0-9]+', doc_string).__getitem__(0)[8:]
        doc_string = json.dumps(doc_json)
        action_string = f'{{\"index\":{{"_id": "{doc_id}" }}}}'
        bulk_string = bulk_string + action_string + "\n" + doc_string + "\n"
        number_of_doc_in_bulk += 1
        if (number_of_doc_in_bulk % 1000) == 0:
            response = requests.post(f"http://localhost:9200/{index}/_bulk",
                                     data=bulk_string.encode("UTF-8"),
                                     headers={"Content-Type": "application/json; charset=utf-8"})
            print(response)
            response_json = json.loads(response.content.decode('utf-8'))
            # if response_json['error']:
            #     raise Exception('problem')

            bulk_string = ''
            print('inserted {number_of_doc_in_bulk}')


def decide_on_collaboration(artist_1_birth, artist_1_death, artist_2_birth, artist_2_death):
    # They both live, they could work on a song
    if artist_1_birth != 'None' and artist_2_birth != 'None' and artist_1_death == 'None' and artist_2_death == 'None':
        return 'Based on our information, they both are still alive. So the could have collaborated in the past.. '
    # Second one is younger, they could work on a song
    elif artist_1_birth == 'None' or artist_2_birth == 'None':
        return 'We cant tell.'
    elif artist_1_birth <= artist_2_birth <= artist_1_death:
        return 'They could collaborate. '
    # Second one is older, they cold work on a song
    elif artist_2_birth <= artist_1_birth <= artist_2_death:
        return 'They could collaborate. '
    # They could not work on a song
    else:
        return 'We have no information about them. '


def main_elastic():
    # data = load_data()
    # insert_data(data)
    index = 'artists'

    # Enter names of two artists
    artist_1 = str(input("Enter a name for a first artist: "))
    artist_2 = str(input("Enter a name for a second artist: "))

    result_1 = search_by_name(index, artist_1)
    result_2 = search_by_name(index, artist_2)

    # Get needed attributes
    artist_1_birth = result_1['date_of_birth']
    artist_1_death = result_1['date_of_death']
    artist_2_birth = result_2['date_of_birth']
    artist_2_death = result_2['date_of_death']

    print(decide_on_collaboration(artist_1_birth, artist_1_death, artist_2_birth, artist_2_death))
    statistical_analysis('VINF_final_output/input3.txt')


if __name__ == "__main__":
    main_elastic()
