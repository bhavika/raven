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
    endpoint = 'me/following'

    for i in range(len(artist_ids)):
        data['ids'] = artist_ids[i:i+49]
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        requests.put(r.spotify.prefix+endpoint, headers=headers, params=params)

path = 'Library.csv'
follow(filename=path)
