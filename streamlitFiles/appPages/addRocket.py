import streamlit as st
import os
from rocketpy import Rocket


def app():
    rocketTab, aeroTab, parachuteTab = st.tabs(
        ["Create a Rocket", "Aerodynamic Surfaces", "Recovery Configuration"]
    )

    with rocketTab:
        with st.container():
            rocketName = st.text_input("Rocket Name", value="Rokit")
            radius = st.number_input(
                "Outer Radius (m)", value=127 / 2000, min_value=0.0, format="%f"
            )
            mass = st.number_input(
                "Dry Mass (Kg)",
                value=16.241,
                min_value=0.0,
                format="%f",
                help="Rocket's mass without propellant in kg.",
            )
            inertiaI = st.number_input(
                "Unloaded longitudenal moment of inertia (Kg*m^2)",
                value=6.6,
                format="%f",
                help="Rocket's moment of inertia, without propellant, with respect to to an axis perpendicular to the rocket's axis of cylindrical symmetry, in kg*m^2.",
            )
            inertiaZ = st.number_input(
                "Unloaded rotational moment of inertia (Kg*m^2)",
                value=0.0351,
                format="%f",
                help="Rocket's moment of inertia, without propellant, with respect to the rocket's axis of cylindrical symmetry, in kg*m^2.",
            )
            distanceRocketNozzle = st.number_input(
                "(Unloaded) Distance between CG and Nozzle Exit (m)",
                value=-1.255,
                format="%f",
                help="Distance between rocket's center of mass, without propellant, to the exit face of the nozzle, in meters.",
            )

            distanceRocketPropellant = st.number_input(
                "(Unloaded) Distance between Rocket CG and and Motor CG",
                value=-0.85704,
                format="%f",
                help="Distance between rocket's center of mass, without propellant, to the motor reference point, which for solid and hybrid motors is the center of mass of solid propellant, in meters.",
            )
            col1, col2 = st.columns(2)
            with col1:
                with st.container():

                    powerOffDrag = st.file_uploader(
                        label="Power off Drag Curve Data",
                        help="Rocket's drag coefficient as a function of Mach number when the motor is off. Can be found via rasAero (2 column data: mach number and poweroffDrag, keep mach number upto 2)",
                        type=["csv"],
                    )
                    if powerOffDrag is not None:
                        with open(
                            os.path.join(
                                "streamlitFiles\__pycache__", powerOffDrag.name
                            ),
                            "wb",
                        ) as f:
                            f.write(powerOffDrag.getbuffer())
                            powerOffDrag = os.path.join(
                                "streamlitFiles\__pycache__", powerOffDrag.name
                            )
                        st.success("File Uploaded")

            with col2:
                with st.container():
                    powerOnDrag = st.file_uploader(
                        label="Power off Drag Curve Data",
                        help="Rocket's drag coefficient as a function of Mach number when the motor is on. Can be found via rasAero (2 column data: mach number and powerOnDrag, keep mach number upto 2)",
                        type=["csv"],
                    )

                    if powerOnDrag is not None:
                        with open(
                            os.path.join(
                                "streamlitFiles\__pycache__", powerOnDrag.name
                            ),
                            "wb",
                        ) as f:
                            f.write(powerOnDrag.getbuffer())
                            powerOnDrag = os.path.join(
                                "streamlitFiles\__pycache__", powerOnDrag.name
                            )
                        st.success("File Uploaded")
            if "rocketInitialized" not in st.session_state:
                st.session_state.rocketInitialized = False
            motor = st.session_state.motor
            rocketSubmitted = st.button("Submit")
            if rocketSubmitted == True or st.session_state.rocketInitialized == True:
                rokit = Rocket(
                    motor=motor,
                    radius=radius,
                    mass=mass,
                    inertiaI=inertiaI,
                    inertiaZ=inertiaZ,
                    distanceRocketNozzle=distanceRocketNozzle,
                    distanceRocketPropellant=distanceRocketPropellant,
                    powerOffDrag=powerOffDrag,
                    powerOnDrag=powerOnDrag,
                )
                st.session_state.rocketInitialized = True

                st.success("Rocket Added")
                with aeroTab:
                    setRailButtons = st.slider(
                        "Set Rail button position relative to CG",
                        -5.0,
                        5.0,
                        (-0.5, 0.2),
                        step=0.01,
                        help="Two values which represent the distance of each of the two rail buttons to the center of mass of the rocket without propellant. If the rail button is positioned above the center of mass, its distance should be a positive value. If it is below, its distance should be a negative value. The order does not matter. All values should be in meters.",
                    )
                    setRailButtons = list(setRailButtons)
                    rokit.setRailButtons(setRailButtons)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        noseLength = st.number_input(
                            "Add Nosecone Length",
                            value=0.55829,
                            min_value=0.0,
                            format="%f",
                            help="Nose cone length or height in meters. Must be a positive value.",
                        )
                        noseKind = st.selectbox(
                            "Nosecone Shape Type",
                            options=("Von Karman", "conical", "ogive", " lvhaack"),
                        )
                        noseDistanceToCM = st.number_input(
                            "Distance between unloaded rocket CM and base of nose",
                            min_value=0.0,
                            value=0.71971,
                            format="%f",
                            help="Nose cone position relative to rocket unloaded center of mass, considering positive direction from center of mass to nose cone. Consider the center point belonging to the nose cone base to calculate distance.",
                        )

                        rokit.addNose(
                            length=noseLength,
                            kind=noseKind,
                            distanceToCM=noseDistanceToCM,
                        )

                    with col2:
                        # finShape= st.selectbox("Fin Shape Type:", options=("Trapezoidal", "Elliptical"))
                        st.write("Adding Trapezoidal finset")
                        finCount = st.number_input(
                            "# of Fins", min_value=0, value=4, format="%d"
                        )
                        finSpan = st.number_input(
                            "Fin Span",
                            min_value=0.0,
                            value=0.1,
                            format="%f",
                            help="Fin Span/Height in meters",
                        )
                        finRC = st.number_input(
                            "Root length",
                            min_value=0.0,
                            value=0.12,
                            format="%f",
                            help="Fin Root Length in meters",
                        )
                        finTC = st.number_input(
                            "Tip length",
                            min_value=0.0,
                            value=0.04,
                            format="%f",
                            help="Fin Tip Length in meters",
                        )
                        finDistanceToCM = st.number_input(
                            "Distance between unloaded rocket CM and base of nose",
                            min_value=0.0,
                            value=0.71971,
                            format="%f",
                            help="Fin set position relative to rocket unloaded center of mass, considering positive direction from center of mass to nose cone. Consider the center point belonging to the top of the fins to calculate distance.",
                        )
                        rokit.addFins(
                            finCount,
                            finSpan,
                            finRC,
                            finTC,
                            finDistanceToCM,
                            radius=0,
                            cantAngle=0,
                        )
                        # if finShape == "Trapezoidal":
                        #     rokit.addFin(
                        #         finCount,
                        #         finSpan,
                        #         finRC,
                        #         finTC,
                        #         finDistanceToCM,
                        #         radius=0,
                        #         cantAngle=0,
                        #     )
                        # else:
                        #     rokit.addEllipticalFins(finCount, finRC, finSpan, finDistanceToCM, cantAngle=)

                    with col3:
                        st.number_input

            # else:
            #     with aeroTab:
            #         st.warning("Initialize rocket first")
            #     with parachuteTab:
            #         st.warning("Initialize rocket first")
