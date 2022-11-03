from cgi import test
import streamlit as st
from rocketpy import Flight


st.write(
    st.session_state.rocketInfo["deploymentHeight"],
    " ",
    st.session_state.rocketInfo["mainLag"],
)
st.write(st.session_state.rocket.parachutes[:])
tf = st.button("simulate")

if tf:
    testFlight = Flight(
        rocket=st.session_state.rocket,
        environment=st.session_state.Env,
        inclination=85,
        heading=0,
    )
    # testFlight.allInfo()
