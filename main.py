import streamlit as st
import utils as utl
import pandas as pd
import os
import base64
from views import beat_the_line, home,recommendation

path = os.getcwd()

st.set_page_config(layout="centered", page_title='MLB At Bat Predictor', page_icon=":baseball:")
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# background

image_path = f"{path}/data/image.png"
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
    }}
    </style>
    '''
    return style

st.write(background_image_style(image_path), unsafe_allow_html=True)



def navigation():
    route = utl.get_current_route()
    if route == "home":
        home.load_view()
    elif route == "Recommendation":
        recommendation.load_view()
    elif route == "Beat the line":
        beat_the_line.load_view()
    elif route == None:
        home.load_view()

navigation()
