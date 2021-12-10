import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
from PIL import Image
import requests

### Setting up authorization to access API ###
auth_manager = SpotifyClientCredentials("3e935e832ff04b5c89d3ab4ac28982b1","cf4809789e63467e8c44d608df670c53")
sp = spotipy.Spotify(auth_manager=auth_manager)

class get_info():
    '''
    Set up class containing attributes and methods for API access

    ...

    Attributes
    ----------
    user: str
        Input username
    PL: str
        Input playlist name

    Methods
    -------
    show_playlists():
        Returns a dict pairing the user's public playlist names and their accompanying uri identifications
    get_pl_cover():
        Returns a PIL Image object of the specified playlist's cover art
    select_songs():
        Returns

    '''
    def __init__(self,username,playlist_name):
        self.user = username
        self.PL = playlist_name
    def show_playlists(self):
        playlists = sp.user_playlists(self.user)
        playlist_names = np.array([playlists["items"][i]["name"] for i in range(len(playlists["items"]))])
        playlist_uris = np.array([playlists["items"][i]["uri"] for i in range(len(playlists["items"]))])
        dicts = {}
        for j in range(len(playlist_uris)):
            dicts[playlist_names[j]] = playlist_uris[j]
        return dicts
    def get_pl_cover(self):
        dicts = self.show_playlists()
        if (self.PL).startswith("spotify:"):
            pl = self.PL
        else:
            pl = dicts[self.PL]
        covs = sp.playlist_cover_image(pl)
        response = requests.get(covs[0]["url"],stream=True)
        im = Image.open(response.raw)
        #im = crop_im(req_out=response)
        #im = im.resize((660,660))
        return im

    def select_songs(self):
        dicts = self.show_playlists()
        if (self.PL).startswith("spotify:"):
            pl = self.PL
        else:
            pl = dicts[self.PL]
        tracks = sp.playlist_items(pl)
        track_names = np.array([tracks["items"][i]["track"]["name"] for i in range(len(tracks["items"]))])
        track_uris = np.array([tracks["items"][i]["track"]["uri"] for i in range(len(tracks["items"]))])
        #tr_dicts = {}
        #for j in range(len(track_uris)):
            #tr_dicts[track_names[j]] = track_uris[j]
        return track_uris,track_names

    def extract_features(self):
        #songs = select_songs(username,playlist_name)[0]
        #songs = (self.select_songs())[0]
        #names = select_songs(username,playlist_name)[1]
        #names = (self.select_songs())[1]
        songs, names = self.select_songs()
        df = pd.DataFrame()
        df["name"] = names

        features = sp.audio_features(songs)
        f_df=pd.DataFrame.from_dict(features)
        df = pd.merge(df,f_df,left_index=True, right_index=True)
        df = df.drop(["type","track_href","analysis_url"],axis=1)
        return df





