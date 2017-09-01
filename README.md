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

1) Install Python 3.4.3
2) Install Git through your terminal

    Mac OS X: `brew install git`
    
    Fedora: `sudo dnf install git-all` 
    
    Debian: `sudo apt-get install git-all`
3) Clone this repository with `git clone https://github.com/bhavika/raven.git`
4) Navigate into the `raven` directory with `cd raven`
5) Install the required libraries: `pip install -r requirements.txt`
6) Create an app on the [Spotify Developer Console](https://developer.spotify.com/my-applications/#!/).

   Click on Create an App and fill in the following: 
   
   Application Name: raven
   
   Redirect URIs: http://locahost/
   
   Click on Save. 
   
   Copy the Client ID and Client Secret. 
7) Navigate into the `raven` directory where you cloned the repository. 
8) Create a file and name it `.env`, refer to the `sample.env` for the format.
   Populate the SPOTIPY_REDIRECT_URI, USERNAME, SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET from step 1.
   
   Save the `.env` file.

### Run:

The first time you run any of these commands, you'll be taken to spotify.com to authenticate Raven and get an
access token. Once you approve the permissions, copy the new URL from your browser window (should be of the form 
localhost?code=<TOKEN>) and paste it into the terminal where you ran the raven command after the prompt & hit Enter. 

Every time the access token expires, you'll be required to reauthenticate Raven with Spotify. 

##### Open a terminal in the `raven` directory and try the following.

Follow all artists from a CSV file (look at format.csv)

    python main.py follow '/path/to/your/CSV/file'

Unfollow all artists from a CSV file (look at format.csv)

    python main.py unfollow '/path/to/your/csv/file'

Add a bunch of songs to a playlist from a CSV file (look at format.csv)

    python main.py add-tracks playlist '/path/to/your/csv/file'

Add a bunch of songs to a playlist from cached search results (track_ids)

[Note: When you're specifying source as cache, the filename argument is not needed.]

    python main.py add-tracks playlist --source=cache

Add a bunch of songs to your library from a CSV file (look at format.csv)

    python main.py add-tracks library '/path/to/your/csv/file'
   
Add a bunch of songs to to your library from the cached search results (track_ids)
    
    python main.py add-tracks library --source=cache

### Features:

- Follow all artists from a CSV file.
- Unfollow all artists from a CSV file.
- Add a list of songs (CSV) to a new playlist or library.