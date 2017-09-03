#!/usr/bin/env python

import os
import requests
from tqdm import tqdm
import logging
from raven.constants import *
from raven.raven import Raven

logging.getLogger("requests").setLevel(logging.WARNING)


def follow(filename):
    r = Raven()
    artist_ids = r.search_artist_ids(filename)
    data = {}
    payload_size = 49
    size = len(artist_ids)

    if size < payload_size:
        data['ids'] = artist_ids
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        response = requests.put(url=r.spotify.prefix+follow_endpoint, headers=r.headers, params=params)
        return response

    else:
        x = [artist_ids[i: i+payload_size] for i in range(0, len(artist_ids), payload_size)]
        for chunk in x:
            data['ids'] = chunk
            params = (
                ('type', 'artist'),
                ('ids', ','.join(data['ids']))
            )
            response = requests.put(url=r.spotify.prefix+follow_endpoint, headers=r.headers, params=params)


def add_tracks(location, filename=None, source='library'):
    r = Raven()
    payload_size = 49

    if str(source) == 'cache':
        track_ids = [line.rstrip('\n') for line in open('.cache-{0}-tracks.txt'.format(os.environ['USERNAME']), 'r')]
    else:
        if os.path.isfile(filename):
            track_ids = r.search_song_ids(filepath=filename)
        else:
            print("Invalid file path entered. Try again.")
            exit()

    username = os.environ['USERNAME']
    size = len(track_ids)

    track_uris = [TRACK_URI_FORMAT + track_id for track_id in track_ids]

    if location == 'playlist':
        playlist_title = input("Enter a name for your playlist ")

        public = input("Make this playlist public? (yes/no) ").lower()
        if public.startswith('y'):
            public = 'true'
        else:
            public = 'false'
        new_playlist = r.spotify.user_playlist_create(user=username, name=playlist_title, public=public)
        playlist_id = new_playlist["id"]

        endpoint = playlist_add_endpoint.format(user_id=username, playlist_id=playlist_id)

        # Bypass rate limiting - push < 50 items per request
        if size < payload_size:
            params = (
                ('position', 0),
                ('uris', ','.join(track_uris))
            )
            requests.post(url=r.spotify.prefix + endpoint, headers=r.headers, params=params)
        else:
            x = [track_uris[i: i+payload_size] for i in range(0, size, payload_size)]
            for chunk in tqdm(x):
                params = (
                    ('position', 0),
                    ('uris', ','.join(chunk))
                )
                requests.post(url=r.spotify.prefix+endpoint, headers=r.headers, params=params)

    elif location == 'library':
        if size < payload_size:
            r.spotify.current_user_saved_tracks_add(tracks=track_ids)
        else:
            for i in tqdm(range(size)):
                x = track_ids[i:i + payload_size]
                r.spotify.current_user_saved_tracks_add(tracks=x)


def unfollow(filename):
    r = Raven()
    artist_ids = r.search_artist_ids(filename)
    data = {}

    size = len(artist_ids)

    if size < 49:
        data['ids'] = artist_ids
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        requests.delete(url=r.spotify.prefix + follow_endpoint, headers=r.headers, params=params)

    else:
        x = [artist_ids[i: i + 49] for i in range(0, size, 49)]
        for chunk in tqdm(x):
            data['ids'] = chunk
            params = (
                ('type', 'artist'),
                ('ids', ','.join(data['ids']))
            )
            requests.delete(url=r.spotify.prefix + follow_endpoint, headers=r.headers, params=params)
