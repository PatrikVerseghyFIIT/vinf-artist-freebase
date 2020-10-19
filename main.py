import gzip
import re
import time
import pandas as pd
from datetime import datetime

deceased_dates_path = '/home/patrik/Downloads/milion/deceased_persons.gz'
birth_dates_path = '/home/patrik/Downloads/milion/births.gz'
names_path = '/home/patrik/Downloads/milion/names.gz'
artists_path = '/home/patrik/Downloads/milion/artists.gz'


def remove_duplicates_list_dictionary(list_of_dictionary):
    seen = set()
    new_list = []
    for d in list_of_dictionary:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_list.append(d)
    return new_list


def create_artists_data_frame(path):
    artists = []
    f = gzip.open(path, 'r')
    for line in f:
        dict = {}
        str_line = str(line)
        pattern = 'g.(.+?)>'
        result = re.search(pattern, str_line)
        if result:
            found = result.group(1)
            dict['id'] = found
        artists.append(dict)
    return artists


def create_date_data_frame(path, name):
    Births = []
    f = gzip.open(path, 'r')
    for line in f:
        Dict = {}
        str_line = str(line)
        #print(str_line)
        id_pattern = 'g.(.+?)>'
        m = re.search(id_pattern, str_line)
        if m:
            found = m.group(1)
            #print(found)
            Dict['id'] = found
        n = re.search('"(.+?)"', str_line)
        if n:
            found1 = n.group(0)
            found1 = re.sub('["]', '', found1)
        #    print(found1)
            Dict[name] = found1
        Births.append(Dict)
    return Births


def get_attribute_by_id(type_of_attribute, id, dataframe):
    filter = dataframe['id'] == id
    result_filter = dataframe[filter]
    return result_filter.iloc[0][type_of_attribute]


def change_date_format(date):
    if pd.isna(date):
        return date
    date = str(date)
    if len(str(date)) == 4:
        date = date + '-01-01'
    date = datetime.strptime(date, '%Y-%m-%d')
    return date


def decide_on_collaboration(artist1, artist2, dataframe):
    artist_1_name = get_attribute_by_id('name', artist1, dataframe)
    artist_2_name = get_attribute_by_id('name', artist2, dataframe)

    artist_1_birth = get_attribute_by_id('date_of_birth', artist1, dataframe)
    artist_1_death = get_attribute_by_id('date_of_death', artist1, dataframe)

    artist_2_birth = get_attribute_by_id('date_of_birth', artist2, dataframe)
    artist_2_death = get_attribute_by_id('date_of_death', artist2, dataframe)

    result = 'Artists: ' + artist_1_name + ', ' + artist_2_name + '. Dates(B/D): ' + \
             str(artist_1_birth) + '/' + str(artist_1_death) + ', ' + str(artist_2_birth) + '/' + str(artist_2_death)


    # They both live, they could work on a song
    if pd.isna(artist_1_death) and pd.isna(artist_2_death):
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


def main():
    # Get list of dictionaries for each attribute and remove duplicates within them
    date_of_births = create_date_data_frame(birth_dates_path, 'date_of_birth')
    date_of_births = remove_duplicates_list_dictionary(date_of_births)

    date_of_deaths = create_date_data_frame(deceased_dates_path, 'date_of_death')
    date_of_deaths = remove_duplicates_list_dictionary(date_of_deaths)

    names = create_date_data_frame(names_path, 'name')
    names = remove_duplicates_list_dictionary(names)

    artists = create_artists_data_frame(artists_path)
    artists = remove_duplicates_list_dictionary(artists)

    # Create dataframes from list of dictionaries
    df_births = pd.DataFrame(date_of_births)
    df_deaths = pd.DataFrame(date_of_deaths)
    df_names = pd.DataFrame(names)
    df_artists = pd.DataFrame(artists)

    # Merging dataframes
    result = pd.merge(df_births, df_deaths, on='id', how='left')
    result2 = pd.merge(result, df_names, on='id')
    final_dataframe = pd.merge(result2, df_artists, on='id')
    final_dataframe = final_dataframe.drop_duplicates(subset=['id'], keep='first')
    print(final_dataframe)

    # Unify date formats
    final_dataframe['date_of_birth'] = final_dataframe['date_of_birth'].apply(lambda x: change_date_format(x))
    final_dataframe['date_of_death'] = final_dataframe['date_of_death'].apply(lambda x: change_date_format(x))

    # Enter artist id
    artist_id_1 = str(input("Enter first artist ID"))
    artist_id_2 = str(input("Enter second artist ID"))

    # Decide if the entered artists could work on a song together
    print(decide_on_collaboration(artist_id_1, artist_id_2, final_dataframe))
if __name__ == "__main__":
    # execute only if run as a script
    main()
