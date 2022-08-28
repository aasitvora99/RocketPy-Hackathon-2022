import rocketpy
from datetime import timezone
import datetime
from asyncio.windows_events import NULL
import matplotlib
import streamlit as st
import pandas as pd
from rocketpy import Environment

print()
print()
print()
print(rocketpy.__version__)
print()
print()
print()


# matplotlib.use('tkagg')
# for notebook commands, find streamlit alternative
# %config InlineBackend.figure_formats = ['svg']
# %matplotlib inline


# @st.cache(suppress_st_warning=True)
def app():
    railLength = st.number_input("What's the size of Launch Rail?")
    latitude = st.number_input(
        "Latitude of the place you're launching",
        min_value=-180.0,
        max_value=180.0,
        step=1e-12,
        format="%.5f",
    )
    longitude = st.number_input(
        "Longitude of the place you're launching",
        min_value=-180.0,
        max_value=180.0,
        step=1e-12,
        format="%.5f",
    )
    # Mapping feature: for later work
    # df = pd.DataFrame(([latitude, longitude]), columns=[
    #                   'latitude', 'longitude'])
    # st.map(df)

    elevation = st.number_input("What's the mean sea level elevation in meters?")
    wenHop = st.date_input("When are you launching (in UTC)")
    # wenHopTime = st.time_input("What time are you launching? (in UTC)")
    # dt = wenHopTime(datetime.timezone.utc)
    # utc_time = wenHopTime.replace(tzinfo=timezone.utc)
    # utc_timestamp = utc_time.timestamp()

    Env123 = Environment(
        railLength=railLength,
        latitude=latitude,
        longitude=longitude,
        elevation=elevation,
    )
    # launchDate = wenHop + datetime.datetime(utc_timestamp)
    # Hour given in UTC time
    Env123.setDate((wenHop.year, wenHop.month, wenHop.day, 12))
    atmosModel = st.selectbox(
        "Define an Atmospheric Model for Environment Setup",
        (
            "Forecast",
            "WyomingSounding",
            "NOAARucSounding",
            "StandardAtmosphere",
            "Reanalysis",
            "Ensemble",
        ),
    )

    if atmosModel == "Forecast":
        file_type = st.selectbox(
            "Specify Location of Data", ("GFS", "FV3", "RAP", "NAM")
        )
    elif atmosModel == "Ensemble":
        file_type = st.selectbox("Specify Location of Data", ("GEFS", "CMC"))
    else:
        file_type = ""

    if file_type == "":
        Env123.setAtmosphericModel(type=atmosModel)
    else:
        Env123.setAtmosphericModel(type=atmosModel, file=file_type)

    # environmentTable = Env.allInfoReturned()
    # environmentTable = Env123.allInfoReturned()
    print(rocketpy.Environment.allInfoReturned(Env123))
    # environmentTable = Env.allPlotInfoReturned()
    # print(environmentTable)
    # if st.button("Run Environment Simulation"):
    #     st.table(print(environmentTable))
