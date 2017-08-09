#!/usr/bin/env python

from raven import Raven
import requests
import os
import fire


def follow(filename):
    r = Raven()
    artist_ids = r.search_artist_ids(filename)
    data = {}
    endpoint = 'me/following'

    for i in range(len(artist_ids)):
        data['ids'] = artist_ids[i:i+49]
        params = (
            ('type', 'artist'),
            ('ids', ','.join(data['ids']))
        )
        requests.put(url=r.spotify.prefix+endpoint, headers=r.headers, params=params)


def add_songs(location, filename):
    r = Raven()
    track_ids = r.search_song_ids(filepath=filename)
    if location == 'playlist':
        playlist_title = input("Enter a name for your playlist")
        public = input("Make this playlist public? (yes/no)").lower()
        if public.startswith('y'):
            public = 'true'
        data = dict(name=playlist_title, public=False, description="Created automatically by Raven from {}".
                    format(filename))
        # Submit a playlist creation request, read response & get playlist ID
        endpoint = 'users/{user_id}/playlists/{playlist_id}/tracks'.format(user_id=os.getenv('USERNAME'))


if __name__ == '__main__':
    fire.Fire()