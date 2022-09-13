import streamlit as st
from appPages import home
from appPages import addEnvironment
from appPages import addMotor
from appPages import addRocket
from appPages import Results
import os

# os.chdir('../docs/notebooks')
landing = st.container()


# def main():
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


# if __name__ == "__main__":
#     main()
