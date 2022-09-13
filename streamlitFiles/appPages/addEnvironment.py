from cgi import test
import rocketpy
from datetime import timezone
import datetime
from asyncio.windows_events import NULL
import matplotlib
import streamlit as st
import pandas as pd
from rocketpy import Environment

# from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
# from threading import current_thread
# from contextlib import contextmanager
from io import StringIO
import sys
import logging
import time
import numpy as np


# matplotlib.use('tkagg')
# for notebook commands, find streamlit alternative
# %config InlineBackend.figure_formats = ['svg']
# %matplotlib inline


# @st.cache(suppress_st_warning=True)
# @contextmanager
# def st_redirect(src, dst):
#     placeholder = st.empty()
#     output_func = getattr(placeholder, dst)

#     with StringIO() as buffer:
#         old_write = src.write

#         def new_write(b):
#             if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
#                 buffer.write(b + "")
#                 output_func(buffer.getvalue() + "")
#             else:
#                 old_write(b)

#         try:
#             src.write = new_write
#             yield
#         finally:
#             src.write = old_write


# @contextmanager
# def st_stdout(dst):
#     "this will show the prints"
#     with st_redirect(sys.stdout, dst):
#         yield


# @contextmanager
# def st_stderr(dst):
#     "This will show the logging"
#     with st_redirect(sys.stderr, dst):
#         yield


# def printFunction():
#     """
#     Returns terminal outputs for function
#     :return:
#     """
#     if st.button("Run Environment Simulation"):
#         st.text()


# if __name__ == "__main__":
#     with st_stdout("success"), st_stderr("code"):
#         printFunction()


# def displayInfo(dict test):
#     st.text("Launch Site Details")
#     st.code("Launch Rail length: \t", test["launch_rail_length"])


def app():
    railLength = st.number_input("What's the size of Launch Rail in meters?", value=5.2)
    latitude = st.number_input(
        "Latitude of the place you're launching",
        value=32.9901,
        min_value=-180.0,
        max_value=180.0,
        step=1e-12,
        format="%.5f",
    )
    longitude = st.number_input(
        "Longitude of the place you're launching",
        value=-106.974998,
        min_value=-180.0,
        max_value=180.0,
        step=1e-12,
        format="%.5f",
    )
    # Mapping feature: for later work
    # df = pd.DataFrame(([latitude, longitude]), columns=[
    #                   'latitude', 'longitude'])
    # st.map(df)

    elevation = st.number_input(
        "What's the mean sea level elevation in meters?", value=1400
    )
    wenHop = st.date_input("When are you launching (in UTC)")
    # wenHopTime = st.time_input("What time are you launching? (in UTC)")
    # dt = wenHopTime(datetime.timezone.utc)
    # utc_time = wenHopTime.replace(tzinfo=timezone.utc)
    # utc_timestamp = utc_time.timestamp()

    Env = Environment(
        railLength=railLength,
        latitude=latitude,
        longitude=longitude,
        elevation=elevation,
    )
    # launchDate = wenHop + datetime.datetime(utc_timestamp)
    # Hour given in UTC time
    Env.setDate((wenHop.year, wenHop.month, wenHop.day, 12))
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
        Env.setAtmosphericModel(type=atmosModel)
    else:
        Env.setAtmosphericModel(type=atmosModel, file=file_type)
    lsd, amd, sac = st.tabs(
        [
            "Launch Site Details",
            "Atmospheric Model Details",
            "Surface Atmospheric Conditions",
        ]
    )
    environmentTableDict = dict(Env.allInfoReturned())
    if st.button("Run Environment Simulation"):
        with lsd:
            st.write(
                "Launch Rail length: \t",
                environmentTableDict["launch_rail_length"],
                " m",
            )
            st.write("Launch Date: \t", environmentTableDict["launch_date"], " UTC")
            st.write("Launch Site Latitude: \t", environmentTableDict["lat"], " °")
            st.write("Launch Site Longitude: \t", environmentTableDict["lon"], " °")
            # df = pd.DataFrame([latitude, longitude], columns=["lat", "lon"])
            # df = {"lat": latitude, "lon": longitude}
            st.write(
                "Launch Site UTM coordinates: ",
                environmentTableDict["initialEast"],
                " ",
                environmentTableDict["initialEW"],
                "\t",
                environmentTableDict["initialNorth"],
                " ",
                environmentTableDict["initialHemisphere"],
            )
            st.write("Reference Datum: \t", environmentTableDict["datum"])

            st.write(environmentTableDict)
            df = pd.DataFrame(
                np.random.randn(1, 2) / [25, 25] + [latitude, longitude],
                columns=["lat", "lon"],
            )  # still figuring out how this works, 25,25 seems to be the area wrt the lat and long, and idk how random pays a role here just picked from the documentation
            st.map(df)

    # environmentTable = Env.allPlotInfoReturned()
    # print(environmentTable)
    # if st.button("Run Environment Simulation"):
    #     st.table(print(environmentTable))


# {
#     "grav": 9.80665,
#     "launch_rail_length": 6,
#     "elevation": 1.019374966621399,
#     "modelType": "Forecast",
#     "modelTypeMaxExpectedHeight": "78862.84",
#     "windSpeed": 7.686906814575195,
#     "windDirection": 236.54574584960938,
#     "windHeading": 56.545753479003906,
#     "surfacePressure": 1000,
#     "surfaceTemperature": 284.6130676269531,
#     "surfaceAirDensity": 1.2240052212166865,
#     "surfaceSpeedOfSound": 338.1990494702038,
#     "launch_date": "2022-12-09 12:00:00",
#     "lat": 65,
#     "lon": 35,
#     "initDate": "2022-12-09 00:00:00",
#     "endDate": "2022-28-09 00:00:00",
#     "interval": 3,
#     "initLat": -90,
#     "endLat": 90,
#     "initLon": 0,
#     "endLon": 359.75,
# }
