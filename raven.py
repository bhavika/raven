import csv
import logging
import os
import spotipy
from time import sleep
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Raven(object):

    logging.basicConfig(filename='Raven.log', level=logging.DEBUG)

    def __init__(self):
        token = os.environ['TOKEN']
        if token:
            self.spotify = spotipy.Spotify(auth=token)
            self.spotify.trace = True
            self.spotify.prefix = 'https://api.spotify.com/v1/'
            self.headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + token
            }
        else:
            print("Token not set in environment.")

    def search_artist_ids(self, filepath):
        """
        Find Spotify Artist IDs for all unique artists from a CSV file
        :param filepath: str
        :return list of artist IDs
        """

        artists = create_collection(filepath, item_type='artists')
        artist_ids = set()
        ignored = set()

        for artist in artists:
            try:
                results = self.spotify.search(q='artist:'+artist, type='artist', limit=3)
                id = str(results['artists']['items'][0]['id'])
                artist_ids.add(id)
                sleep(0.1)
            except IndexError:
                ignored.add(artist)
                logging.info("Ignored: ", artist)
                sleep(0.4)

        return list(artist_ids)

    def search_song_ids(self, filepath):
        """
        Find Spotify song ID for all the tracks from a CSV file
        :param filepath: str
        :return: list of song IDs
        """

        tracks = create_collection(filepath, item_type='tracks')
        track_ids = set()
        ignored = set()

        for track in tracks:
            try:
                results = self.spotify.search(q=track, type='track', limit=3)
                id = str(results['tracks']['items'][0]['id'])
                track_ids.add(id)
                sleep(0.1)
            except IndexError:
                ignored.add(track)
                logging.info("Ignored: ", track)
                sleep(0.4)

        return list(track_ids)


def create_collection(filepath, item_type='artists'):
    with open(filepath) as f:
        reader = csv.DictReader(f, fieldnames=['Artist', 'Song'], delimiter=',')
        next(reader)
        items = set()
        for row in reader:
            artist = row['Artist'].strip()
            if item_type == 'Song':
                song = row['Song'].strip()
                items.add(song + " " + artist)
            else:
                items.add(artist)
    return items