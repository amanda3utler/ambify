import streamlit as st
import numpy as np
from ambify.analysis import run_classifier
import pygame as pg

pg.mixer.init()

st.title("ambify")
user = st.text_input("Username")
pl_name = st.text_input("Playlist")

if 'vol' not in st.session_state:
    st.session_state['vol'] = 0.4

vol = st.slider('Volume',0.0,1.0,value=st.session_state.vol,step=0.1)

def get_vol(val):
    if val == 5:
        return 0.2
    elif val == 4:
        return 0.3
    elif (val == 1) or (val == 7):
        return 0.7
    else:
        return "Default"

@st.cache
def get_vibe(u_n,pl_n):
    metric = run_classifier(u_n,pl_n)
    head = 'sounds/s_'
    so_ext = ".mp3"
    aud = pg.mixer.music.load(head+str(metric)+so_ext)
    pg.mixer.music.play(-1)
    best_v = get_vol(metric)
    return metric, best_v

if (user != "") and (pl_name != ""):
    with st.spinner(text="Loading your vibe..."):
        m = get_vibe(u_n=user,pl_n=pl_name)
        st.text("Recommended volume = "+str(m[1]))

pg.mixer.music.set_volume(vol)


stopped = st.button("Stop")

if stopped == True:
    pg.mixer.music.stop()
    stopped == False
    st.text("Enter a new playlist to continue")
