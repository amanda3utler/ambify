# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from ambify.login import get_info
import numpy as np
import statistics as st
import collections as c
import pandas as pd


# %%
def classify_sg(song_row):
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

class mode_dat():
    '''
    #If the mode is equal or only differs by 1 instance, perform a tiebreak
    '''
    def __init__(self,arr):
        self.data = np.array(arr)
    def top_two(self):
        m1 = c.Counter(self.data).most_common()[0][0]
        m2 = c.Counter(self.data).most_common()[1][0]
        return (m1,m2)
    def mode_cts(self):
        mt,mt2 = self.top_two()
        inst = len(np.where(self.data == mt)[0])
        inst2 = len(np.where(self.data == mt2)[0])
        return (inst,inst2)
    def secondary(self):
        mt, mt2 = self.top_two()
        s_rank = [0,7,2,3,1,6,4,5]
        for s in s_rank:
            if s in [mt, mt2]:
                return s

def run_classifier(username,playlist):
    sobj = get_info(username,playlist)
    sdf = sobj.extract_features()
    fts = []
    for i in range(len(sdf)):
        svar = classify_sg(sdf.loc[i])
        fts.append(svar)
    if len(fts) > 1:
        md = mode_dat(fts)
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












        
        



