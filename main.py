import gzip
import re
import zipfile

deceased_dates_path = 'date_of_deaths.txt'
birth_dates_path = 'date_of_births.txt'
names_path = 'names.txt'
zip_file_name = '/home/patrik/Downloads/freebase-100-mil.zip'
file_name = 'freebase-head-100000000'


def decide_on_collaboration(artist1, artist2):
    artist_1_name = get_attribute_by_id(names_path, artist1)
    artist_2_name = get_attribute_by_id(names_path, artist2)

    artist_1_birth = fix_date(get_attribute_by_id(birth_dates_path, artist1))
    artist_1_death = fix_date(get_attribute_by_id(deceased_dates_path, artist1))

    artist_2_birth = fix_date(get_attribute_by_id(birth_dates_path, artist2))
    artist_2_death = fix_date(get_attribute_by_id(deceased_dates_path, artist2))

    result = 'Artists: ' + artist_1_name + ', ' + artist_2_name + '. Dates(B/D): ' + \
             str(artist_1_birth) + '/' + str(artist_1_death) + ', ' + str(artist_2_birth) + '/' + str(artist_2_death)

    # They both live, they could work on a song
    if artist_1_death == 'NotFound' and artist_2_death == 'NotFound':
        return 'They could work on a song. ' + result
    # Second one is younger, they could work on a song
    elif artist_2_birth >= artist_1_birth and artist_2_birth <= artist_1_death:
        return 'They could work on a song. ' + result
    # Second one is older, they cold work on a song
    elif artist_1_birth >= artist_2_birth and artist_1_birth <= artist_2_death:
        return 'They could work on a song. ' + result
    # They could not work on a song
    else:
        return 'They could not work on a song. ' + result


def create_artist():
    final_f = open('final_artist.txt', 'r+')
    f = open('vinf_artist.txt', 'r')
    for artist_id in f:
        if not check_if_string_in_file(final_f, str(artist_id)):
            write_id = artist_id[:len(artist_id) - 1]
            write_birth = get_attribute_by_id(birth_dates_path, write_id)
            print(write_id)
            if write_birth != 'NotFound':
                write_name = get_attribute_by_id(names_path, write_id)
                if write_name != 'NotFound':
                    write_death = get_attribute_by_id(deceased_dates_path, write_id)
                    final_f.write(write_id + '; ')
                    final_f.write(write_name + '; ')
                    final_f.write(fix_date(write_birth) + '; ')
                    final_f.write(fix_date(write_death) + '\n')


def get_attribute_by_id(path, id):
    f = open(path, 'r')
    for line in f:
        id_pattern = '(g.'+id+')>'
        m = re.search(id_pattern, line)
        if m:
            found = m.group(1)
            if found == 'g.'+id:
                n = re.search('"(.+?)"', line)
                if n:
                    found1 = n.group(0)
                    found1 = re.sub('["]', '', found1)
                    return found1
    return 'NotFound'


def fix_date(date):
    if len(date) == 4:
        date = date + '-01-01'
    return date


def check_if_string_in_file(read_obj, string_to_search):
    read_obj.seek(0, 0)
    for line in read_obj:
        if string_to_search in line:
            read_obj.seek(2)
            return True
    return False


def get_artist_file():
    artists_f = open('vinf_artist.txt', 'r+')
    with zipfile.ZipFile(zip_file_name) as myzip:
        with myzip.open(file_name) as myfile:
            for line in myfile:
                str_line = str(line)
                pattern_artist = '<http://rdf.freebase.com/ns/music.artist>'
                result_artist = re.search(pattern_artist, str_line)
                if result_artist:
                    pattern_id = '<http://rdf.freebase.com/ns/g.(.+?)>'
                    result_id = re.search(pattern_id, str_line)
                    if result_id:
                        artist_id = result_id.group(1)
                        if not check_if_string_in_file(artists_f, str(artist_id)):
                            artists_f.write(artist_id + '\n')
    myfile.close()
    myzip.close()


def get_artist_name_dates():
    date_of_births_f = open('date_of_births.txt', 'r+')
    date_of_deaths_f = open('date_of_deaths.txt', 'r+')
    names_f = open('names.txt', 'r+')

    with zipfile.ZipFile(zip_file_name) as myzip:
        with myzip.open(file_name) as myfile:
            for line in myfile:
                str_line = line.decode('utf-8')
                pattern_name = '<http://rdf.freebase.com/ns/type.object.name>'
                pattern_date_of_birth = '<http://rdf.freebase.com/ns/people.person.date_of_birth>'
                pattern_date_of_death = '<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>'
                result_name = re.search(pattern_name, str_line)
                result_date_of_birth = re.search(pattern_date_of_birth, str_line)
                result_date_of_death = re.search(pattern_date_of_death, str_line)
                if result_name:
                    names_f.write(str_line + '\n')
                if result_date_of_birth:
                    date_of_births_f.write(fix_date(str_line) + '\n')
                if result_date_of_death:
                    date_of_deaths_f.write(fix_date(str_line) + '\n')
    myfile.close()
    myzip.close()
    date_of_births_f.close()
    date_of_deaths_f.close()
    names_f.close()


def main():
    # get a file which contains only artists
    get_artist_file()
    # get files of names,dates of birth and dates of death
    get_artist_name_dates()
    # get only relevant information
    create_artist()

    # Enter IDs of both artists
    artist_id_1 = str(input("Enter first artist ID"))
    artist_id_2 = str(input("Enter second artist ID"))

    # Decide if the entered artists could work on a song together
    print(decide_on_collaboration(artist_id_1, artist_id_2))


if __name__ == "__main__":
    main()
