import streamlit as st
from rocketpy import Motor
import os
import pandas as pd


def app():
    # simCheck = False
    # if simCheck == True:
    #     thrustSource = None
    motorList = {}
    for root, dir, files in os.walk("data\motors"):
        for file in files:
            filePath = os.path.join(root, file)
            motorList.update({file[:-4]: filePath})  # -4 for removing .eng from name

    thrustSource = st.selectbox("Pick an Engine", options=motorList.keys())
    thrustSource = motorList[thrustSource]
    st.write(thrustSource)
    # thrustSource = st.file_uploader(label="Upload Engine File")
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

    if st.button("Simulate"):
        col1, col2, col3 = st.columns(3)

        with st.container():

            with col1:
                st.subheader("Nozzle Details")
                st.write("Nozzle Radius (m)", rokit.nozzleRadius)
                st.write("Nozzle Throat Radius (m)", rokit.throatRadius)

            with col2:
                st.subheader("Grain Details")
                st.write("Number of Grains", rokit.grainNumber)
                st.write("Grain Spacing (m)", rokit.grainSeparation)
                st.write("Grain Density (kg/m3)", rokit.grainDensity)
                st.write("Grain Mass (kg)", rokit.grainInitialMass)
                st.write("Grain Outer Radius (m)", rokit.grainOuterRadius)
                st.write("Grain Inner Radius (m)", rokit.grainInitialInnerRadius)
                st.write("Grain Height (m)", rokit.grainInitialHeight)
                st.write("Grain Volume (cm3)", (rokit.grainInitialVolume * 1000000))

            with col3:
                st.subheader("Motor Details")
                st.write("Total Burning Time: ", rokit.burnOutTime, " s")
                st.write("Total Propellant Mass: ", rokit.propellantInitialMass, " Kg")
                st.write("Propellant Exhaust Velocity: ", rokit.exhaustVelocity, "m/s")
                st.write("Average Thrust: ", rokit.averageThrust, " N")
                st.write(
                    "Maximum Thrust: ",
                    rokit.maxThrust,
                    " N at ",
                    rokit.maxThrustTime,
                    " s after ignition",
                )
                st.write("Total Impulse: ", rokit.totalImpulse, " Ns")

        col4, col5, col6, col7 = st.columns(4)
        with col4:

            rokit.allInfo()
            st.write("Thrust(N) x Time(s)")
            thrustDF = pd.DataFrame(
                rokit.thrust.source[:, 1], index=rokit.thrust.source[:, 0]
            )
            thrustDF.columns = ["Thrust (N)"]
            st.line_chart(thrustDF, use_container_width=True)

            st.write("Grain Height (M) x Time(s)")
            grainHeightDF = pd.DataFrame(
                rokit.grainHeight.source[:, 1],
                index=rokit.grainHeight.source[:, 0],
            )
            grainHeightDF.columns = ["Grain Height (M)"]
            st.line_chart(grainHeightDF, use_container_width=True)

            st.write("Propellant Inertia I (Kg*M^2) x Time(s)")
            inertiaIDF = pd.DataFrame(
                rokit.inertiaI.source[:, 1],
                index=rokit.inertiaI.source[:, 0],
            )
            inertiaIDF.columns = ["Propellant Inertia I (Kg*M^2)"]
            st.line_chart(inertiaIDF, use_container_width=True)

        with col5:

            st.write("Propellant Total Mass (Kg) x Time(s)")
            massDF = pd.DataFrame(
                rokit.mass.source[:, 1], index=rokit.mass.source[:, 0]
            )
            massDF.columns = ["Propellant Total Mass (Kg)"]
            st.line_chart(massDF, use_container_width=True)

            st.write("Burn Rate (M/s) x Time(s)")
            burnRateDF = pd.DataFrame(
                rokit.burnRate.source[:, 1],
                index=rokit.burnRate.source[:, 0],
            )
            burnRateDF.columns = ["Burn Rate (M/s)"]
            st.line_chart(burnRateDF, use_container_width=True)

            st.write("Propellant Inertia I Dot (Kg*M^2/s) x Time(s)")
            inertiaIDotDF = pd.DataFrame(
                rokit.inertiaIDot.source[:, 1],
                index=rokit.inertiaIDot.source[:, 0],
            )
            inertiaIDotDF.columns = ["Propellant Inertia I Dot (Kg*M^2/s)"]
            st.line_chart(inertiaIDotDF, use_container_width=True)

        with col6:

            st.write("Mass Dot (Kg/S) x Time(s)")
            massDotDF = pd.DataFrame(
                rokit.massDot.source[:, 1], index=rokit.massDot.source[:, 0]
            )
            massDotDF.columns = ["Mass Dot (Kg/S)"]
            st.line_chart(massDotDF, use_container_width=True)

            st.write("Burn Area (M^2) x Time(s)")
            burnAreaDF = pd.DataFrame(
                rokit.burnArea.source[:, 1],
                index=rokit.burnArea.source[:, 0],
            )
            burnAreaDF.columns = ["Burn Area (M^2)"]
            st.line_chart(burnAreaDF, use_container_width=True)

            st.write("Propellant Inertia Z (Kg*M^2) x Time(s)")
            inertiaZDF = pd.DataFrame(
                rokit.inertiaZ.source[:, 1],
                index=rokit.inertiaZ.source[:, 0],
            )
            inertiaZDF.columns = ["Propellant Inertia Z (Kg*M^2)"]
            st.line_chart(inertiaZDF, use_container_width=True)

        with col7:

            st.write("Grain Inner Radius (M) x Time(s)")
            grainInnerRadiusDF = pd.DataFrame(
                rokit.grainInnerRadius.source[:, 1],
                index=rokit.grainInnerRadius.source[:, 0],
            )
            grainInnerRadiusDF.columns = ["Grain Inner Radius (M)"]
            st.line_chart(grainInnerRadiusDF, use_container_width=True)

            st.write("Kn (M^2/M^2) x Grain Inner Radius(M)")
            KnDF = pd.DataFrame(
                rokit.Kn.source[:, 1],
                index=rokit.Kn.source[:, 0],
            )
            KnDF.columns = ["Kn (M^2/M^2)"]
            st.line_chart(KnDF, use_container_width=True)

            st.write("Propellant Inertia Z Dot (Kg*M^2/s) x Time(s)")
            inertiaZDotDF = pd.DataFrame(
                rokit.inertiaZDot.source[:, 1],
                index=rokit.inertiaZDot.source[:, 0],
            )
            inertiaZDotDF.columns = ["Propellant Inertia Z Dot (Kg*M^2/s)"]
            st.line_chart(inertiaZDotDF, use_container_width=True)


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
