#!/usr/bin/env python

import os
import requests
from tqdm import tqdm
from raven.constants import *
from raven.raven import Raven


def follow(filename):
    r = Raven()
    artist_ids = r.search_artist_ids(filename)
    data = {}

    for i in tqdm(range(len(artist_ids))):
        data['ids'] = artist_ids[i:i+49]
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        requests.put(url=r.spotify.prefix+follow_endpoint, headers=r.headers, params=params)


def add_tracks(location, filename):
    r = Raven()
    track_ids = r.search_song_ids(filepath=filename)
    username = os.environ['USERNAME']
    size = len(track_ids)

    if location == 'playlist':
        track_uris = [TRACK_URI_FORMAT + track_id for track_id in track_ids]

        playlist_title = input("Enter a name for your playlist ")

        public = input("Make this playlist public? (yes/no) ").lower()
        if public.startswith('y'):
            public = 'true'
        else:
            public = 'false'
        new_playlist = r.spotify.user_playlist_create(user=username, name=playlist_title, public=public)
        playlist_id = new_playlist["id"]

        endpoint = playlist_add_endpoint.format(user_id=username, playlist_id=playlist_id)

        # Rate limiting - push 50 items per request
        if size < 49:
            params = (
                ('position', 0),
                ('uris', ','.join(track_uris))
            )
        else:
            for i in tqdm(range(size)):
                x = track_uris[i:i + 49]
                params = (
                    ('position', 0),
                    ('uris', ','.join(x))
                )

        requests.put(url=r.spotify.prefix+endpoint, headers=r.headers, params=params)

    elif location == 'library':

        if size < 49:
            r.spotify.current_user_saved_tracks_add(tracks=track_ids)
        else:
            for i in tqdm(range(size)):
                x = track_ids[i:i+49]
                r.spotify.current_user_saved_tracks_add(tracks=x)


def unfollow(filename):
    r = Raven()
    artist_ids = r.search_artist_ids(filename)
    data = {}

    for i in tqdm(range(len(artist_ids))):
        data['ids'] = artist_ids[i:i+49]
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        requests.delete(url=r.spotify.prefix+follow_endpoint, headers=r.headers, params=params)
