import streamlit as st
import numpy as np
from ambify.analysis import run_classifier
from ambify.outputs.visuals import crop_im
from ambify.outputs.visuals import get_colors
import pygame as pg
import requests
from PIL import Image
import time

st.markdown('<style>body{background-color: darkgreen;}</style>',unsafe_allow_html=True)

pg.mixer.init()
original_title = '<p style="font-family:Georgia; color:darkgreen; font-size: 40px;">ambify</p>'
st.markdown(original_title, unsafe_allow_html=True)
quote = '<p style="font-family:sans-serif; color:grey; font-size: 15px;font-style: italic;">vibe your life</p>'
st.markdown(quote,unsafe_allow_html=True)
user = st.text_input("Username")


with st.form(key='Playlist'):
    text_input = st.text_input(label='Enter a playlist or type "RANDOM"')
    submit = st.form_submit_button(label='Get my ambience!')
    if (text_input != "") and (user != "") and (text_input != "RANDOM"):
        met_out = str(run_classifier(user,text_input))
        if met_out == "flag":
            st.text("Playlist empty, please check spelling.")
        else:
            lpath = "ambify/outputs/visuals/palettes/test"+met_out+"_L.gif"
            rpath = "ambify/outputs/visuals/palettes/test"+met_out+"_R.gif"

            im = crop_im(us_name=user, pl_name=text_input)
        #nupath = "https://htmlcolorcodes.com/assets/images/colors/aqua-color-solid-background-1920x1080.png"
        #with Image.open(requests.get(nupath, stream=True).raw) as image:
            #im3 = image.rotate(90)
            #im3 = im3.crop((0, 0, 800, 710))

            col1, col2, col3 = st.columns([1, 1.45, 1])
            with col1:
                st.image(lpath)
            with col2:
                st.image(im)
            with col3:
                st.image(rpath)

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
        return " Default"

head = 'ambify/outputs/sounds/s_'
so_ext = ".mp3"

@st.cache
def get_vibe(u_n,pl_n,c):
    count = c
    metric = run_classifier(u_n,pl_n)
    if metric == "flag":
        pass
    else:
        best_v = get_vol(metric)
        aud = pg.mixer.music.load(head + str(metric) + so_ext)
        pg.mixer.music.play(-1)
        return metric, best_v, count

if (submit!= False) and (text_input == ""):
    pg.mixer.music.pause()
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
        st.text("Recommended volume =" + str(m[1]))
        st.session_state["count"] += 1
        #Counter assist tool:
        #st.text(m[2])

pg.mixer.music.set_volume(vol)

stopped = st.button("Stop Audio")

if stopped == True:
    pg.mixer.music.pause()
    st.session_state["count"] +=1
    stopped = False
    st.text("Submit a playlist to continue")
