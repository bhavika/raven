#!/usr/bin/env python

from raven import Raven
import requests
import os


def follow(filename):
    r = Raven()
    token = os.getenv('TOKEN')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    artist_ids = r.search_artist_ids(filename)
    data = {}
    data['ids'] = list(artist_ids)
    endpoint = 'me/following'
    params = (
        ('type', 'artist'),
        ('ids', ','.join(data['ids']))
    )
    r = requests.put(r.spotify.prefix+endpoint, headers=headers, params=params)

filename='/home/bhavika/Music/sample.csv'
follow(filename=filename)