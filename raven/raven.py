import csv
import json
import logging
import os
from datetime import timedelta, datetime
import spotipy
from spotipy import oauth2
from spotipy import util
from spotipy.client import SpotifyException
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv
from raven.constants import scope

load_dotenv(find_dotenv())

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(filename='Raven.log', filemode='a', level=logging.DEBUG)


class Raven(object):

    def __init__(self):
        token = util.prompt_for_user_token(os.environ['USERNAME'], scope=scope,
                                           client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                           client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                           redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'))
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

    def refresh_token(self):
        filename = '.cache-' + os.environ['USERNAME']
        with open(filename) as f:
            token = json.load(f)

        if 'expires_at' not in token or \
                timedelta(minutes=0) == token['expires_at'] - int(datetime.now().strftime("%s")):

            sp_oauth = oauth2.SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                           client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                           redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                                           scope=scope)

            if sp_oauth._is_token_expired(token):
                refresh_token = token['refresh_token']
                token = sp_oauth.refresh_access_token(refresh_token)

        return spotipy.Spotify(auth=token['access_token'])

    def search_artist_ids(self, filepath):
        """
        Find Spotify Artist IDs for all unique artists from a CSV file
        :param filepath: str
        :return list of artist IDs
        """
        artists = self.create_collection(filepath, item_type='artists')
        print("{} artists found".format(len(artists)))
        artist_ids = set()
        ignored = set()

        for artist in tqdm(artists):
            while True:
                try:
                    results = self.spotify.search(q='artist:' + artist, type='artist', limit=3)
                    aid = str(results['artists']['items'][0]['id'])
                    artist_ids.add(aid)
                    logging.info("Added artist ID for: {} ".format(artist))
                except IndexError:
                    ignored.add(artist)
                    logging.debug("Ignored: {}".format(artist))
                except ConnectionError:
                    continue
                except SpotifyException as e:
                    logging.debug(e.__str__())
                    self.refresh_token()

        return list(artist_ids)

    def search_song_ids(self, filepath):
        """
        Find Spotify track ID for all the tracks from a CSV file
        :param filepath: str
        :return: list of track IDs
        """
        tracks = self.create_collection(filepath, item_type='tracks')
        print("{} tracks found".format(len(tracks)))
        track_ids = set()
        ignored = set()

        with open('.cache-{0}-tracks.txt'.format(os.environ['USERNAME']), 'w') as track_cache:
            for track in tqdm(tracks):
                try:
                    results = self.spotify.search(q=track, type='track', limit=3)
                    tid = str(results['tracks']['items'][0]['id'])
                    track_ids.add(tid)
                    track_cache.write(tid + '\n')
                    logging.info("Added track ID for: {} ".format(track))
                except IndexError:
                    ignored.add(track)
                    logging.debug("Ignored: {}".format(track))
                except ConnectionError:
                    continue
                except SpotifyException as e:
                    self.refresh_token()
                    logging.debug(e.__str__())
        return list(track_ids)

    def create_collection(self, filepath, item_type):
        with open(filepath) as f:
            reader = csv.DictReader(f, fieldnames=['Artist', 'Track'], delimiter=',')
            next(reader)
            items = set()
            for row in tqdm(reader):
                artist = row['Artist'].strip()
                if item_type == 'tracks':
                    track = row['Track'].strip()
                    items.add(track + " " + artist)
                else:
                    items.add(artist)
        return items
