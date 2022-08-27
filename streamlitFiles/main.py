import streamlit as st
from pages import home
from pages import addEnvironment
from pages import addMotor
from pages import addRocket
from pages import Results
import os

# os.chdir('../docs/notebooks')
landing = st.container()

# Adding Navigation Pages
with landing:
    PAGES = {
        "Home Page": home,
        "Add Environment": addEnvironment,
        "Add Motor": addMotor,
        "Design Rocket": addRocket,
        "Results": Results,
    }

    st.sidebar.title("RocketPy")

    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()
