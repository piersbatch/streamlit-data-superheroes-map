"""
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "C:\PYTHON\Streamlit_dashboard.png"
cd C:\PYTHON\streamlit\st_dashboard_generator
python -m streamlit run "C:\PYTHON\streamlit\st_dashboard_generator\app.py"
"""

import streamlit as st
import os 

#-----------------------------------------
# Import necessary libraries
import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit page configuration
st.set_page_config(layout="wide")

# Add header image to the top of the page
st.image("https://raw.githubusercontent.com/piersbatch/streamlit-data-superheroes-map/main/Header.png")

# Streamlit app title
# st.title("Snowflake Data Superheroes Map")

# Load the data from the CSV file
data = pd.read_csv("Data Superhero Location.csv")
st.info("After zooming in, untick to show larger point sizes ☑")

# Check if the necessary columns exist
if "latitude" in data.columns and "longitude" in data.columns and "Sex" in data.columns:

    # Create a color function for sex
    def assign_color(sex):
        # Baby blue for Males, brick orange for Females, both with 50% opacity
        return [41, 181, 232, 128] if sex == 'M' else [125, 68, 207, 128]

    data["color"] = data["Sex"].apply(assign_color)

    # Define the map layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=1000,  # Show a large pin for each city with a data superhero
        pickable=True,
    )

    # Add a checkbox to toggle point size
    show_large_points = st.checkbox("Show Larger Point Size", value=1)


    # Set point size based on checkbox state
    if show_large_points:
        layer.get_radius = 40000
    else:
        layer.get_radius = 1000

    # Display the map
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state={
            "latitude": 20,
            "longitude": 0,
            "zoom": 1.5,
            "pitch": 0
        },
        tooltip={
            "html": "<b>Full Name:</b> {Full Name}<br/><b>Company:</b> {Company}<br/><b>Location:</b> {Location (State, Country)}",
            "style": {
                "backgroundColor": "#11567f",
                "color": "white"
            }
        },
        # Setting the map to a light style
        map_style="mapbox://styles/mapbox/light-v10",
        height=850  # Adjusting the height of the map
    ))

    # Display table without certain columns below the map
    columns_to_display = ["Full Name", "Company", "Location (State, Country)", "Sex"]
    st.write(data[columns_to_display])

else:
    st.error("Data must have 'latitude', 'longitude', and 'Sex' columns!")
