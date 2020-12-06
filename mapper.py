#!/usr/bin/env python
"""mapper.py"""

import sys
import re


for line in sys.stdin:
    str_line = str(line)
    pattern_artist = '<http://rdf.freebase.com/ns/music.artist>'
    result_artist = re.search(pattern_artist, str_line)
    if result_artist:
        pattern_id = '<http://rdf.freebase.com/ns/(.+?)>'
        result_id = re.search(pattern_id, str_line)
        if result_id:
            artist_id = result_id.group(1)
            print(artist_id + '\n')
