### IMPORTS ###
from ambify.login import Get_info
import numpy as np
import statistics as st
import collections as c
import pandas as pd

def classify_sg(song_row):
    '''
    A function that classifies a single song row from the extract_features dataset to determine the output vibe of that song

    The vibes are assigned as follows:
    0: somber and mellow songs
    1: happier, upbeat songs that are not extremely acoustic nor electronic
    2: highly acoustic but generally happier sounding songs
    3: energetic songs that have darker, more brooding tendencies, and high acousticness
    4: chill, happier songs with more electronic qualities
    5: energetic and more heavily processed songs
    6: energetic songs with darker, more brooding tendencies and low acousticness
    7: heavily processed songs that are broody or temperate

    Each song is classified as one of the above on the basis of three features: valence, energy, acousticness

    Parameters
    ----------
    song_row: int
        The index of a pandas.DataFrame row

    Returns
    -------
    clfd: int
        The output vibe assigned as one of the integers above
    '''
    v = song_row["valence"]
    ac = song_row["acousticness"]
    E = song_row["energy"]
    if (v <= .3) and (E <= 0.3):
        clfd = 0
    elif (v <= .3) and (E >= 0.3):
        if ac < .5:
            clfd = 6
        else:
            clfd = 3
    elif (.3 < v < .5):
        if ac < .3:
            clfd = 7
        elif (.3 <= ac <= .8):
            if E > .5:
                clfd = 4
            else:
                clfd = 1
        else:
            clfd = 2
    elif (.3 < v < .5) and (E > .7):
        clfd = 1
    elif (v >= .5):
        if ac < .2:
            clfd = 5
        else:
            clfd = 4
    else:
        clfd = 5
    return clfd

class Mode_dat():
    '''
    A class to handle analysis if a single classification is not possible across a whole playlist (equal modes)

    ...

    Attributes
    ----------
    data: numpy.ndarray
        Returns the input array

    Methods
    -------
    top_two():
        Returns the most-found and second most-found elements in an array (if equal modes, returns equal values)
    mode_cts():
        Returns the number of instances that each of the top two modes appears
    secondary():
        Performs a secondary form of classification based on the top two modes. See below for more details.
    '''
    def __init__(self,arr):
        '''
        Sets data attribute

        Parameters
        ----------
        arr: array-like
            Input array of the classification output for each song in a playlist
        '''
        self.data = np.array(arr)
    def top_two(self):
        '''
        Returns the most-found and second most-found elements in an array (if equal modes, returns equal values)

        Returns
        -------
        (m1,m2): tuple
            The mode and the mode if all instances of the first mode value were removed from the array
        '''
        m1 = c.Counter(self.data).most_common()[0][0]
        m2 = c.Counter(self.data).most_common()[1][0]
        return (m1,m2)
    def mode_cts(self):
        '''
        Returns the number of instances that each of the top two modes appears

        Returns
        -------
        (inst,inst2): tuple
            inst: the number of times the mode appears
            inst2: the number of times the second-next mode appears
        '''
        mt,mt2 = self.top_two()
        inst = len(np.where(self.data == mt)[0])
        inst2 = len(np.where(self.data == mt2)[0])
        return (inst,inst2)
    def secondary(self):
        '''
        A function that uses only the top two modes to classify the playlist

        This function implements a ranking of the possible mode outcomes based on how general they are.
        For example, output 0, which outputs a gentle rain audio in the output phase of ambify,is ranked first since
        it is more applicable to more playlists than the sounds of party chatter (output 7), which is ranked last.
        All 7 outputs are ranked in this manner based off the corresponding visuals and outputs.
        This allows for safe classification outcome if there is not a single mode present for a playlist.

        Returns:
        -------
        s: int
            The classification output if this function is run
        '''
        mt, mt2 = self.top_two()
        s_rank = [0,7,2,3,1,6,4,5]
        for s in s_rank:
            if s in [mt, mt2]:
                return s

def run_classifier(username,playlist):
    '''
    A function that classifies an entire playlist given a username and playlist name.
    Each song in a playlist is classified, and the mode across all songs determines the overall classification.
    If no single mode is found or the number of songs deciding a mode only leads by 1 song,
    the secondary classifier is run.

    Parameters
    ----------
    username: str
        Spotify username
    playlist: str
        The Spotify playlist name or playlist URI

    Returns
    -------
    outc:int or str
        The classifcation outcome for the whole playlist; str if playlist is empty
    '''
    sobj = Get_info(username,playlist)
    sdf = sobj.extract_features()
    fts = []
    for i in range(len(sdf)):
        svar = classify_sg(sdf.loc[i])
        fts.append(svar)
    if len(fts) > 1:
        md = Mode_dat(fts)
        c1,c2 = md.mode_cts()
        if c2-c1 > 1:
            outc = st.mode(fts)
        else:
            outc = md.secondary()
    elif len(fts) == 1:
        outc = st.mode(fts)
    else:
        outc = "flag"
    return outc












        
        



