import csv
import streamlit as st
from rocketpy import Motor


def app():
    st.write("hello world")
    thrustSource = st.file_uploader(label="Upload Engine File")
    burnOut = st.number_input(
        "Motor Burnout (s)", value=3.9, min_value=0.0, format="%f"
    )
    grainNumber = st.number_input("Number of Grains", value=5, min_value=1, format="%d")
    grainSeparation = st.number_input(
        "Grain Separation (m)",
        value=(5 / 1000),
        min_value=0.0,
        format="%f",
        help="Distance between two grains in meters.",
    )
    grainDensity = st.number_input(
        "Grain Density (kg/m^3)",
        value=1815.0,
        min_value=0.0,
        format="%f",
        help="Density of each grain in kg/meters cubed.",
    )
    grainOuterRadius = st.number_input(
        "Grain Outer Radius (m)",
        value=(33 / 1000),
        min_value=0.0,
        format="%f",
        help="Outer radius of each grain in meters.",
    )
    grainInitialInnerRadius = st.number_input(
        "Grain Initial Inner Radius (m)",
        value=(15 / 1000),
        min_value=0.0,
        format="%f",
        help="Initial inner radius of each grain in meters.",
    )
    grainInitialHeight = st.number_input(
        "Grain Height (m)",
        value=(120 / 1000),
        min_value=0.0,
        format="%f",
        help="Initial height of each grain in meters.",
    )
    nozzleRadius = st.number_input(
        "Nozzle Radius (m)",
        value=(33 / 1000),
        min_value=0.0,
        format="%f",
        help="Motor's nozzle outlet radius in meters. Used to calculate Kn curve. Optional if the Kn curve is not interesting. Its value does not impact trajectory simulation.",
    )
    throatRadius = st.number_input(
        "Nozzle Throat Radius (m)",
        value=(11 / 1000),
        min_value=0.0,
        format="%f",
        help="Motor's nozzle throat radius in meters. Its value has very low impact in trajectory simulation, only useful to analyze dynamic instabilities, therefore it is optional.",
    )
    interpolationMethod = st.selectbox(
        "Interpolation Method",
        ("linear", "akima", "spline"),
        help="Method of interpolation to be used in case thrust curve is given by data set in .csv or .eng, or as an array.",
    )

    rokit = Motor.SolidMotor(
        thrustSource,
        burnOut,
        grainNumber,
        grainSeparation,
        grainDensity,
        grainOuterRadius,
        grainInitialInnerRadius,
        grainInitialHeight,
        nozzleRadius,
        throatRadius,
        interpolationMethod,
    )
    # if thrustSource == None:
    #     st.button("simulate", disabled=True)
    # else:
    #     if st.button("simulate"):
    #         st.write = rokit.allInfo()
