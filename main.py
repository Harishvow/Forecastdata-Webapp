import streamlit as st
import plotly.express as px
from collections import Counter
from apicall import get_data

st.title("Weather Forecast For Next Days")

place = st.text_input("Enter the name of the place")
days = st.slider("Forecast days", min_value=1, max_value=5)
option = st.selectbox("Select the data to view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [entry["main"]["temp"] for entry in filtered_data]
            dates = [entry["dt_txt"] for entry in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png"
            }
            sky_conditions = [entry["weather"][0]["main"] for entry in filtered_data]
            most_common_condition = Counter(sky_conditions).most_common(1)[0][0]
            st.image(images[most_common_condition], caption=most_common_condition, width=150)

    except KeyError:
        st.error("Invalid place. Please enter a valid city name.")

