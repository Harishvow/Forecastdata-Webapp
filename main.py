import streamlit as st
import plotly.express as px

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
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            print(sky_conditions)
            st.image(image_paths, width=115)
    except KeyError:
        st.write("Invaild Place ")


