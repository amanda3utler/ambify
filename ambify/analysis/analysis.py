# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from ambify.login import extract_features
import numpy as np
import statistics as st


# %%
def classify_sg(song_row):
    v = song_row["valence"]
    ac = song_row["acousticness"]
    E = song_row["energy"]
    if (v <= .3) and (E <= 0.3):
        return 0
    elif (v <= .3) and (E >= 0.3):
        if ac < .6:
            return 6
        else:
            return 3
    elif (.3 < v < .5):
        if ac < .3:
            return 7
        elif (.3 <= ac <= .8):
            if E > .5:
                return 4
            else:
                return 1
        else:
            return 2
    elif (.3 < v < .5) and (E > .7):
        return 1
    elif (v >= .5):
        if ac < .2:
            return 5
        else:
            return 4
    else:
        return 5


# %%
def run_classifier(username,playlist):
    sdf = extract_features(username,playlist)
    fts = []
    for i in range(len(sdf)):
        svar = classify_sg(sdf.loc[i])
        fts.append(svar)
    outc = st.mode(fts)
    return outc


def modes(array):
    array = np.array(array)
    outc = st.mode(array)
    extr = np.array(array[np.where(array != outc)])
    outc2 = st.mode(extr)
    inst = len(np.where(array == outc)[0])
    inst2 = len(np.where(array == outc2)[0])
    return outc, outc2,inst,inst2


# %%
#class tiebreak():
    '''
    If the mode is equal or only differs by 1 instance, perform a tiebreak
    '''
    #def __init__(self,array):
        
        



