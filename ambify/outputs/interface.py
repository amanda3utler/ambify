import streamlit as st
import numpy as np
from ambify.analysis import run_classifier
import pygame as pg

pg.mixer.init()

st.title("ambify")
user = st.text_input("Username")

with st.form(key='Playlist'):
    text_input = st.text_input(label='Enter a playlist or type "RANDOM"')
    submit = st.form_submit_button(label='Get my ambience!')

#pl_name = st.text_input("Playlist")

if 'vol' not in st.session_state:
    st.session_state['vol'] = 0.4

if "count" not in st.session_state:
    st.session_state["count"] = 0

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

head = 'sounds/s_'
so_ext = ".mp3"

@st.cache
def get_vibe(u_n,pl_n,c):
    count = c
    metric = run_classifier(u_n,pl_n)
    best_v = get_vol(metric)
    aud = pg.mixer.music.load(head + str(metric) + so_ext)
    pg.mixer.music.play(-1)
    return metric, best_v, count

if (submit!= False) and (text_input == ""):
    st.text("Don't forget to enter a playlist!")

elif (submit!= False) and (text_input != "RANDOM") and (user == ""):
    st.text("Please enter a username")

elif (submit!= False) and (text_input == "RANDOM"):
    with st.spinner(text="Loading your random vibe..."):
        r = np.random.randint(8)
        st.session_state["count"] += 1
        aud = pg.mixer.music.load(head + str(r) + so_ext)
        pg.mixer.music.play(-1)

elif (user != "") and (submit != False):
    with st.spinner(text="Loading your vibe..."):
        m = get_vibe(u_n=user,pl_n=text_input,c=st.session_state["count"])
        #m = get_vibe(u_n=user, pl_n=pl_name, c=st.session_state["count"])
        st.text("Recommended volume = " + str(m[1]))
        st.session_state["count"] += 1
        #Counter assist tool:
        #st.text(m[2])

pg.mixer.music.set_volume(vol)


stopped = st.button("Stop")

if stopped == True:
    pg.mixer.music.pause()
    st.session_state["count"] +=1
    stopped = False
    st.text("Submit a playlist to continue")
