import streamlit as st
from PIL import Image
import os


def load_view():
    path = os.getcwd()

    st.markdown(f"<h2 style='text-align:center'>Welcome to the MLB At Bat Predictor</h2>", unsafe_allow_html=True)

    # st.markdown(f"<h4 style='text-align:center'>Please make your choice of the two prediction method options:</h4>", unsafe_allow_html=True)

    # st.markdown(f"<h3 style='text-align:left'>Recommendation Mode:</h3>", unsafe_allow_html=True)
    # st.markdown(f"<h5 style='text-align:left'>Probabilty of batter success against the pitcher directly</h5>", unsafe_allow_html=True)

    # st.markdown(f"<h3 style='text-align:left'>Beat the Line Mode:", unsafe_allow_html=True)
    # st.markdown(f"<h5 style='text-align:left'>Probabilty of batter success relative to betting line, recommending hitters when their success probability is higher the line implied probability</h5>", unsafe_allow_html=True)

    image = Image.open(f'{path}/data/Major_League_Baseball_logo.svg.png')
    st.image(image, use_column_width=True, width=1000, output_format="auto")
