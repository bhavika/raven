## Raven [![CircleCI](https://circleci.com/gh/bhavika/raven/tree/master.svg?style=svg)](https://circleci.com/gh/bhavika/raven/tree/master)


CLI tools to manage your Spotify library. 

### Requires:

- Python >3.x 
- spotipy 
- python-dotenv
- fire
- requests
- tqdm 

### Installation:


### Run:

1) Visit this [page](https://developer.spotify.com/web-api/console/post-playlists/) and enter your username,
   select all the scopes necessary (user-follow-modify, user-playlist-modify, playlist-modify-public) then click Get OAuth Token
2) To follow all artists in a CSV file use `python commands.py follow /path/to/your/sample.csv`


### Features:

- Follow all artists from a CSV file.
- Unfollow all artists from a CSV file.
- Add a list of songs (CSV) to a new playlist or library.