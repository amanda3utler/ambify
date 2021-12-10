### IMPORTS ###
import streamlit as st
import numpy as np
from ambify.analysis import run_classifier
from ambify.outputs.visualizer import crop_im
import pygame as pg
import requests
from PIL import Image
import time

### Setting Title ###
st.markdown('<style>body{background-color: darkgreen;}</style>',unsafe_allow_html=True)

### Initializing the pygame mixer which handles audio
pg.mixer.init()

### More title management
original_title = '<p style="font-family:Georgia; color:darkgreen; font-size: 40px;">ambify</p>'
st.markdown(original_title, unsafe_allow_html=True)
quote = '<p style="font-family:sans-serif; color:grey; font-size: 15px;font-style: italic;">vibe your life</p>'
st.markdown(quote,unsafe_allow_html=True)

### Input username
user = st.text_input("Username")

### Setting up streamlit.form to host the playlist information and handle visuals
with st.form(key='Playlist'):
    ### Enter playlist name or "RANDOM!", which returns a randomly generated audio (only)
    text_input = st.text_input(label='Enter a playlist or type "RANDOM"')
    # Submission button
    submit = st.form_submit_button(label='Get my ambience!')
    if (text_input != "") and (user != "") and (text_input != "RANDOM"):
        #Getting the classification for the inputs
        met_out = str(run_classifier(user,text_input))
        if met_out == "flag":
            st.text("Playlist empty, please check spelling.")
        else:
            #Acquiring the visuals
            #These paths specify the panels on either side of the cover art
            lpath = "ambify/outputs/palettes/v"+met_out+"_L.gif"
            rpath = "ambify/outputs/palettes/v"+met_out+"_R.gif"

            # Cropping the cover art
            im = crop_im(us_name=user, pl_name=text_input)

            #Setting up the visuals with st.columns
            col1, col2, col3 = st.columns([1, 1.45, 1])
            with col1:
                st.image(lpath)
            with col2:
                st.image(im)
            with col3:
                st.image(rpath)


#Initializing volume slider to 0.4
if 'vol' not in st.session_state:
    st.session_state['vol'] = 0.4

#Initializing a count metric
if "count" not in st.session_state:
    st.session_state["count"] = 0

vol = st.slider('Volume',0.0,1.0,value=st.session_state.vol,step=0.1)

def get_vol(val):
    '''
    Selects the optimal volume for headphone use for each sound file

    Parameters:
    val: int
        The classifier output
    Returns:
    --------
    "0.2": str
        If val == 5, since audio ambify/outputs/sounds/s_5.mp3 runs a little loud
    "0.3": str
        If val == 4, since audio ambify/outputs/sounds/s_4.mp3 runs a little loud
    "0.7": str
        If (val == 1) or (val == 7) since ambify/outputs/sounds/s_1.mp3 and s_1.mp7 run a little quiet
    "Default": str
        If val any other sound file.
    '''
    if val == 5:
        return "0.2"
    elif val == 4:
        return "0.3"
    elif (val == 1) or (val == 7):
        return "0.7"
    else:
        return "Default"

#Path to sound files
head = 'ambify/outputs/sounds/s_'
so_ext = ".mp3"

#Caching the get_vibe function, so volume adjustment does not cause audio file to restart
@st.cache
def get_vibe(u_n,pl_n,c):
    '''
    Function to classify the playlist again and run the audio
    Parameters:
    -----------
    u_n: str
        Username
    pl_n: str
        Playlist name
    c: int
        Counter input so that the arg inputs are changed slightly and the same playlist can
        be run multiple times in one session. Otherwise, st.cache keeps the function from running.
    Returns
    -------
    metric: int
        Classification outcome
    best_v: str
        Best volume setting for the classification outcome
    count: counter output for testing
    '''
    count = c
    metric = run_classifier(u_n,pl_n)
    best_v = get_vol(metric)
    aud = pg.mixer.music.load(head + str(metric) + so_ext)
    pg.mixer.music.play(-1)
    return metric, best_v, count


### Conditionals to check what inputs a user has given
if (submit!= False) and (text_input == ""):
    pg.mixer.music.pause()
    st.text("Don't forget to enter a playlist!")

elif (submit!= False) and (text_input != "RANDOM") and (user == ""):
    st.text("Please enter a username")

elif (submit!= False) and (text_input == "RANDOM"):
    ### Handling the randomly chosen vibe output
    with st.spinner(text="Loading your random vibe..."):
        r = np.random.randint(8)
        st.session_state["count"] += 1
        aud = pg.mixer.music.load(head + str(r) + so_ext)
        pg.mixer.music.play(-1)

elif (user != "") and (submit != False):
    with st.spinner(text="Loading your vibe..."):
        m = get_vibe(u_n=user,pl_n=text_input,c=st.session_state["count"])
        st.text("Recommended volume = " + str(m[1]))
        st.session_state["count"] += 1

pg.mixer.music.set_volume(vol)

### Stop button for audio
stopped = st.button("Stop Audio")

if stopped == True:
    pg.mixer.music.pause()
    st.session_state["count"] +=1
    stopped = False
    st.text("Submit a playlist to continue")
