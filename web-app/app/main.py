import streamlit as st
import requests
import json
from constants import *
from pathlib import Path

# load gpu specs and game metadata from json files
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'gpu_specs.json', 'r') as f:
    gpu_specs = json.load(f)

with open(BASE_DIR / 'game_metadata.json', 'r') as f:
    game_metadata = json.load(f)


st.title("Game Average FPS Predictor")

# get gpu, game and resolution options for dropdowns
gpu_options = gpu_specs.keys()
game_options = game_metadata.keys()
resolution_options = resolutions.keys()

# api request data dictionary
request_data = {}

# get gpu specs from user input
if not st.checkbox("Use Custom GPU"):
    selected_gpu = st.selectbox("Select GPU", gpu_options, index=4)
    gpu = gpu_specs[selected_gpu]
    for spec in GPU_specs:
        request_data[spec] = gpu[spec]
else:
    # get gpu specs from user input in 3 columns
    left, middle, right = st.columns(3)
    with left:
        request_data['architecture'] = st.selectbox("GPU Architecture", ["None"] + architectures, index=1)
        request_data['boostClock'] = st.number_input("Boost Clock (MHz)", min_value=1777)
        request_data['shaders'] = st.number_input("Number of Shaders", min_value=3584)    
    with middle:
        request_data['tmus'] = st.number_input("Number of TMUs", min_value=112)
        request_data['rops'] = st.number_input("Number of ROPs", min_value=48)
    with right:
        request_data['memorySize'] = st.number_input("Memory Size (GB)", min_value=12)
        request_data['memoryBandwidth'] = st.number_input("Memory Bandwidth (GB/s)", min_value=360)

# get game metadata from user input
if not st.checkbox("Use Custom Game"):
    selected_game = st.selectbox("Select Game", game_options, index=8)
    game = game_metadata[selected_game]
    request_data['Release_Date'] = game['Release_Date']
    for genre in genres:
        request_data[genre] = game[genre]
else:
    # get game release date and genres from user input
    request_data['Release_Date'] = st.number_input("Game Release Date", min_value=2000, value=2020)

    # get genres in 3 columns of checkboxes
    left, middle, right = st.columns(3)
    with left:
        request_data['Adventure'] = st.checkbox("Adventure")
        request_data['Brawler'] = st.checkbox("Brawler")
        request_data['Indie'] = st.checkbox("Indie")
        request_data['Puzzle'] = st.checkbox("Puzzle")
        request_data['RPG'] = st.checkbox("RPG")
    with middle:
        request_data['Racing'] = st.checkbox("Racing")
        request_data['Real Time Strategy'] = st.checkbox("Real Time Strategy")
        request_data['Shooter'] = st.checkbox("Shooter")
        request_data['Simulator'] = st.checkbox("Simulator")
    with right:
        request_data['Sport'] = st.checkbox("Sport")
        request_data['Strategy'] = st.checkbox("Strategy")
        request_data['Tactical'] = st.checkbox("Tactical")
        request_data['Turn Based Strategy'] = st.checkbox("Turn Based Strategy")

# get resolution from user input
if not st.checkbox("Use Custom Resolution"):
    selected_resolution = st.selectbox("Select Resolution", resolution_options, index=1)
    request_data['Resolution'] = resolutions[selected_resolution]
else:
    left, right = st.columns(2)
    with left:
        height = st.number_input("Resolution Width", min_value=0, value=1440)
    with right:
        width = st.number_input("Resolution Height", min_value=0, value=2560)
    request_data['Resolution'] = height * width

# get graphics preset from user input
request_data['Preset'] = st.selectbox("Graphics Preset", ["Low", "Medium", "High", "Ultra"], index=1).lower()

# get prediction api url from secrets
Prediction_API_URL = st.secrets["PREDICTION_API_URL"]

# predict average fps when button is clicked
if st.button("Predict Average FPS"):
    # make api request to prediction endpoint with request_data as json body
    with st.spinner("Connecting to Prediction API..."):
        try:
            response = requests.post(Prediction_API_URL, json=request_data, timeout=10)
            
            # check if response is successful
            response.raise_for_status()

            # get predicted fps from response json
            result = response.json()
            predicted_fps = result.get("prediction", None)

            # display predicted fps to user
            if predicted_fps is not None:
                st.success(f"Predicted Average FPS: {predicted_fps:.2f}")
            else:
                st.error("Prediction API did not return a valid response.")
        
        # handle timeout exception
        except requests.exceptions.Timeout:
            st.error("The request timed out. The server might be running slow. Please try again later.")
        
        # handle http errors
        except requests.exceptions.HTTPError:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")

        # handle json parsing errors
        except (ValueError, KeyError):
            st.error("Failed to parse response. The server didn't return valid prediction JSON.")

        # handle other request exceptions
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")