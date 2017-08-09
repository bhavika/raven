**Raven** [![CircleCI](https://circleci.com/gh/bhavika/raven/tree/master.svg?style=svg)](https://circleci.com/gh/bhavika/raven/tree/master)


CLI tools to manage your Spotify library. 


Run:

1) Go [here](https://developer.spotify.com/web-api/console/post-playlists/) and enter your username,
   select all the scopes necessary (user-follow-modify, user-playlist-modify, playlist-modify-public) then click Get OAuth Token
2) `python commands.py follow -f /path/to/your/sample.csv`


Features:

- Follow all artists from a CSV file


To Do:

- Add a list of songs to your library
- Create a playlist from a CSV/XSPF file
