#!/usr/bin/env python
# coding: utf-8

# In[64]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd


# In[65]:


auth_manager = SpotifyClientCredentials("3e935e832ff04b5c89d3ab4ac28982b1","cf4809789e63467e8c44d608df670c53")
sp = spotipy.Spotify(auth_manager=auth_manager)


# In[66]:


def show_playlists(username):
    playlists = sp.user_playlists(username)
    playlist_names = np.array([playlists["items"][i]["name"] for i in range(len(playlists["items"]))])
    playlist_uris = np.array([playlists["items"][i]["uri"] for i in range(len(playlists["items"]))])
    dicts = {}
    for j in range(len(playlist_uris)):
        dicts[playlist_names[j]] = playlist_uris[j]
    return dicts


# In[67]:


def select_songs(username,playlist_name):
    dicts = show_playlists(username)
    if playlist_name.startswith("spotify:"):
        pl = playlist_name
    else:
        pl = dicts[playlist_name]
    tracks = sp.playlist_items(pl)
    track_names = np.array([tracks["items"][i]["track"]["name"] for i in range(len(tracks["items"]))])
    track_uris = np.array([tracks["items"][i]["track"]["uri"] for i in range(len(tracks["items"]))])
    tr_dicts = {}
    for j in range(len(track_uris)):
        tr_dicts[track_names[j]] = track_uris[j]
    return track_uris,track_names


# In[68]:


def extract_features(username,playlist_name):
    songs = select_songs(username,playlist_name)[0]
    names = select_songs(username,playlist_name)[1]
    df = pd.DataFrame()
    df["name"] = names
    #df["track_id"] = songs
    features = sp.audio_features(songs)
    f_df=pd.DataFrame.from_dict(features)
    df = pd.merge(df,f_df,left_index=True, right_index=True)
    df = df.drop(["type","track_href","analysis_url"],axis=1)
    return df


# In[ ]:




