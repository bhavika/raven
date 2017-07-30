import spotipy
import requests
import csv
import logging
from spotipy.oauth2 import SpotifyClientCredentials
import os

logging.basicConfig(filename='SpotifyManager.log', level=logging.DEBUG)


class SpotifyManager():

    def __init__(self):
        self.client_credentials = SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                           client_secret=os.environ['CLIENT_SECRET'])
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials)

    def search_artist_ids(self, filepath):
        """
         Find Spotify Artist IDs for all unique artists from a CSV file
        :param filepath: String 
        
        """
        with open(filepath) as f:
            reader = csv.DictReader(f, fieldnames=['Artist', 'Song'], delimiter=',')
            artists = set()
            artist_ids = set()

            for row in reader:
                artist = row['Artist'].strip()
                artists.add(artist)

            logging.info("{} artists found!".format(len(artists)))

        for artist in artists:
            results = self.spotify.search(q='artist:'+artist, type='artist', limit=3)
            id = str(results['artists']['items'][0]['id'])
            artist_ids.add(id)


sm = SpotifyManager()
sm.search_artist_ids('/home/bhavika/Music/Library.csv')
