import csv
import logging
import os
import spotipy
from time import sleep


class Raven(object):

    logging.basicConfig(filename='SpotifyManager.log', level=logging.DEBUG)

    def __init__(self):
        token = os.environ['TOKEN']
        if token:
            self.spotify = spotipy.Spotify(auth=token)
            self.spotify.trace = True
            self.spotify.prefix = 'https://api.spotify.com/v1/'

    def search_artist_ids(self, filepath):
        """
        Find Spotify Artist IDs for all unique artists from a CSV file
        :param filepath: String 
        """
        with open(filepath) as f:
            reader = csv.DictReader(f, fieldnames=['Artist', 'Song'], delimiter=',')
            next(reader)
            artists = set()
            artist_ids = set()
            ignored = set()
            for row in reader:
                artist = row['Artist'].strip()
                artists.add(artist)

            logging.info("{} artists found!".format(len(artists)))

        for artist in artists:
            try:
                results = self.spotify.search(q='artist:'+artist, type='artist', limit=3)
                a_id = str(results['artists']['items'][0]['id'])
                artist_ids.add(a_id)
                sleep(0.1)
            except IndexError:
                ignored.add(artist)
                logging.info("Ignored: ", artist)
                sleep(0.4)

        return list(artist_ids)

