import imp
import streamlit as st
from rocketpy import Motor
import os
import pandas as pd
from rocketpy import Rocket


def app():
    # simCheck = False
    # if simCheck == True:
    #     thrustSource = None

    motorList = {}
    for root, dir, files in os.walk("data\motors"):
        for file in files:
            filePath = os.path.join(root, file)
            motorList.update({file[:-4]: filePath})  # -4 for removing .eng from name
    thrustSource = ""
    col1, col2, col3 = st.columns([3, 0.5, 3])
    with col3:
        with st.form("Select Engine Form"):
            thrustSourceList = st.selectbox("Pick an Engine", options=motorList.keys())
            submitted = st.form_submit_button("Submit")
            thrustSource = motorList[thrustSourceList]
            if submitted:
                thrustSource = motorList[thrustSourceList]
                st.write(thrustSource)

    with col2:
        st.write("#  OR")

    with col1:
        with st.form("Upload Engine Form", clear_on_submit=True):
            motorFileUpload = st.file_uploader(label="Upload Engine File", type=["eng"])
            checkboxFlag = st.checkbox("Save to Library")
            # Every form must have a submit button.
            uploaded = st.form_submit_button("Upload")
            if uploaded:
                st.write(
                    "Motor", motorFileUpload.name, "Save to Library: ", checkboxFlag
                )

            if motorFileUpload is not None and checkboxFlag is True:
                fileDetails = {
                    "fileName": motorFileUpload.name,
                    "fileType": motorFileUpload.type,
                }
                st.write(fileDetails)

                with open(os.path.join("data\motors", motorFileUpload.name), "wb") as f:
                    f.write(motorFileUpload.getbuffer())
                thrustSource = os.path.join("data\motors", motorFileUpload.name)

            elif motorFileUpload is not None and checkboxFlag is False:
                with open(
                    os.path.join("streamlitFiles\__pycache__", motorFileUpload.name),
                    "wb",
                ) as f:
                    f.write(motorFileUpload.getbuffer())
                    thrustSource = os.path.join(
                        "streamlitFiles\__pycache__", motorFileUpload.name
                    )

    st.write("Motor Loaded: ", thrustSource[12:-4])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        burnOut = st.number_input(
            "Motor Burnout (s)", value=3.9, min_value=0.0, format="%f"
        )
        grainNumber = st.number_input(
            "Number of Grains", value=5, min_value=1, format="%d"
        )

    with col2:
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

    with col3:

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

    with col4:

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

    with col5:
        grainSeparation = st.number_input(
            "Grain Separation (m)",
            value=(5 / 1000),
            min_value=0.0,
            format="%f",
            help="Distance between two grains in meters.",
        )
        interpolationMethod = st.selectbox(
            "Interpolation Method",
            ("linear", "akima", "spline"),
            help="Method of interpolation to be used in case thrust curve is given by data set in .csv or .eng, or as an array.",
        )
        motir = Motor.SolidMotor(
            thrustSource=thrustSource,
            burnOut=burnOut,
            grainNumber=grainNumber,
            grainSeparation=grainSeparation,
            grainDensity=grainDensity,
            grainOuterRadius=grainOuterRadius,
            grainInitialInnerRadius=grainInitialInnerRadius,
            grainInitialHeight=grainInitialHeight,
            nozzleRadius=nozzleRadius,
            throatRadius=throatRadius,
            interpolationMethod=interpolationMethod,
        )
        motir.zCM = 0
    if st.button("Simulate"):
        if checkboxFlag is False:
            os.remove(thrustSource)
            thrustSource = ""
        col1, col2, col3 = st.columns(3)

        with st.container():

            with col1:
                st.subheader("Nozzle Details")
                st.write("Nozzle Radius (m)", motir.nozzleRadius)
                st.write("Nozzle Throat Radius (m)", motir.throatRadius)

            with col2:
                st.subheader("Grain Details")
                st.write("Number of Grains", motir.grainNumber)
                st.write("Grain Spacing (m)", motir.grainSeparation)
                st.write("Grain Density (kg/m3)", motir.grainDensity)
                st.write("Grain Mass (kg)", motir.grainInitialMass)
                st.write("Grain Outer Radius (m)", motir.grainOuterRadius)
                st.write("Grain Inner Radius (m)", motir.grainInitialInnerRadius)
                st.write("Grain Height (m)", motir.grainInitialHeight)
                st.write("Grain Volume (cm3)", (motir.grainInitialVolume * 1000000))

            with col3:
                st.subheader("Motor Details")
                st.write("Total Burning Time: ", motir.burnOutTime, " s")
                st.write("Total Propellant Mass: ", motir.propellantInitialMass, " Kg")
                st.write("Propellant Exhaust Velocity: ", motir.exhaustVelocity, "m/s")
                st.write("Average Thrust: ", motir.averageThrust, " N")
                st.write(
                    "Maximum Thrust: ",
                    motir.maxThrust,
                    " N at ",
                    motir.maxThrustTime,
                    " s after ignition",
                )
                st.write("Total Impulse: ", motir.totalImpulse, " Ns")

        st.subheader("Plots")
        col4, col5, col6, col7 = st.columns(4)
        with col4:

            # motir.allInfo()
            st.write("Thrust(N) x Time(s)")
            thrustDF = pd.DataFrame(
                motir.thrust.source[:, 1], index=motir.thrust.source[:, 0]
            )
            thrustDF.columns = ["Thrust (N)"]
            st.line_chart(thrustDF, use_container_width=True)

            st.write("Grain Height (M) x Time(s)")
            grainHeightDF = pd.DataFrame(
                motir.grainHeight.source[:, 1],
                index=motir.grainHeight.source[:, 0],
            )
            grainHeightDF.columns = ["Grain Height (M)"]
            st.line_chart(grainHeightDF, use_container_width=True)

            st.write("Propellant Inertia I (Kg*M^2) x Time(s)")
            inertiaIDF = pd.DataFrame(
                motir.inertiaI.source[:, 1],
                index=motir.inertiaI.source[:, 0],
            )
            inertiaIDF.columns = ["Propellant Inertia I (Kg*M^2)"]
            st.line_chart(inertiaIDF, use_container_width=True)

        with col5:

            st.write("Propellant Total Mass (Kg) x Time(s)")
            massDF = pd.DataFrame(
                motir.mass.source[:, 1], index=motir.mass.source[:, 0]
            )
            massDF.columns = ["Propellant Total Mass (Kg)"]
            st.line_chart(massDF, use_container_width=True)

            st.write("Burn Rate (M/s) x Time(s)")
            burnRateDF = pd.DataFrame(
                motir.burnRate.source[:, 1],
                index=motir.burnRate.source[:, 0],
            )
            burnRateDF.columns = ["Burn Rate (M/s)"]
            st.line_chart(burnRateDF, use_container_width=True)

            st.write("Propellant Inertia I Dot (Kg*M^2/s) x Time(s)")
            inertiaIDotDF = pd.DataFrame(
                motir.inertiaIDot.source[:, 1],
                index=motir.inertiaIDot.source[:, 0],
            )
            inertiaIDotDF.columns = ["Propellant Inertia I Dot (Kg*M^2/s)"]
            st.line_chart(inertiaIDotDF, use_container_width=True)

        with col6:

            st.write("Mass Dot (Kg/S) x Time(s)")
            massDotDF = pd.DataFrame(
                motir.massDot.source[:, 1], index=motir.massDot.source[:, 0]
            )
            massDotDF.columns = ["Mass Dot (Kg/S)"]
            st.line_chart(massDotDF, use_container_width=True)

            st.write("Burn Area (M^2) x Time(s)")
            burnAreaDF = pd.DataFrame(
                motir.burnArea.source[:, 1],
                index=motir.burnArea.source[:, 0],
            )
            burnAreaDF.columns = ["Burn Area (M^2)"]
            st.line_chart(burnAreaDF, use_container_width=True)

            st.write("Propellant Inertia Z (Kg*M^2) x Time(s)")
            inertiaZDF = pd.DataFrame(
                motir.inertiaZ.source[:, 1],
                index=motir.inertiaZ.source[:, 0],
            )
            inertiaZDF.columns = ["Propellant Inertia Z (Kg*M^2)"]
            st.line_chart(inertiaZDF, use_container_width=True)

        with col7:

            st.write("Grain Inner Radius (M) x Time(s)")
            grainInnerRadiusDF = pd.DataFrame(
                motir.grainInnerRadius.source[:, 1],
                index=motir.grainInnerRadius.source[:, 0],
            )
            grainInnerRadiusDF.columns = ["Grain Inner Radius (M)"]
            st.line_chart(grainInnerRadiusDF, use_container_width=True)

            st.write("Kn (M^2/M^2) x Grain Inner Radius(M)")
            KnDF = pd.DataFrame(
                motir.Kn.source[:, 1],
                index=motir.Kn.source[:, 0],
            )
            KnDF.columns = ["Kn (M^2/M^2)"]
            st.line_chart(KnDF, use_container_width=True)

            st.write("Propellant Inertia Z Dot (Kg*M^2/s) x Time(s)")
            inertiaZDotDF = pd.DataFrame(
                motir.inertiaZDot.source[:, 1],
                index=motir.inertiaZDot.source[:, 0],
            )
            inertiaZDotDF.columns = ["Propellant Inertia Z Dot (Kg*M^2/s)"]
            st.line_chart(inertiaZDotDF, use_container_width=True)
    return motir


# Nozzle Details
# Nozzle Radius: 0.033 m
# Nozzle Throat Radius: 0.011 m

# Grain Details
# Number of Grains: 5
# Grain Spacing: 0.005 m
# Grain Density: 1815.0 kg/m3
# Grain Outer Radius: 0.033 m
# Grain Inner Radius: 0.015 m
# Grain Height: 0.12 m
# Grain Volume: 0.000 m3
# Grain Mass: 0.591 kg

# Motor Details
# Total Burning Time: 3.9 s
# Total Propellant Mass: 2.956 kg
# Propellant Exhaust Velocity: 2038.745 m/s
# Average Thrust: 1545.218 N
# Maximum Thrust: 2200.0 N at 0.15 s after ignition.
# Total Impulse: 6026.350 Ns
