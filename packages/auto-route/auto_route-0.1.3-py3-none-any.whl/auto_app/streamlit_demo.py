# todo
import os

import streamlit as st
from auto_app import APIAutoApp
st.title("FastAPI Microservices Management")

# Configuration file selection
st.header("Configuration")
config_files = st.multiselect("Select configuration files", os.listdir("."))
environment = st.selectbox("Select environment", ["development", "production"])

api_auto_app = APIAutoApp(config_files)

# Start/stop microservices
st.header("Microservices Control")
start_button = st.button("Start Microservices")
stop_button = st.button("Stop Microservices")

if start_button:
    api_auto_app.run()

if stop_button:
    # Implement logic to stop microservices
    pass

# Additional functionality
st.header("Additional Functionality")
# Add your custom Streamlit components or interactable elements here

