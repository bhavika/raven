**Spotify Manager**

A collection of scripts to manage your Spotify library.

### Requires:

- Python >3.x 
- spotipy 
- python-dotenv
- fire
- requests

### Installation:


### Run:

1) Visit this [page](https://developer.spotify.com/web-api/console/post-playlists/) and enter your username,
   select all the scopes necessary (user-follow-modify, user-playlist-modify, playlist-modify-public) then click Get OAuth Token
2) To follow all artists in a CSV file use `python commands.py follow /path/to/your/sample.csv`


### Features:

- Follow all artists from a CSV file


### To Do:

- Add a list of songs (CSV/XSPF) to a new playlist or library.
- Unfollow artists from a CSV file. 

