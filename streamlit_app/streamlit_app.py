import streamlit as st
import requests


API_URL = 'https://immoeliza-api-66pt.onrender.com/predict'

st.title("ImmoEliza Price Prediction")

# Input form
with st.form("prediction_form"):
    habitableSurface = st.number_input("Habitable Surface (int)", value=200)
    bedroomCount = st.number_input("Bedroom Count (int)", value=3, step=1)

    building_condition_options = {
        1: "1 - To Restore",
        2: "2 - To Renovate",
        3: "3 - Good",
        4: "4 - Just Renovated",
        5: "5 - As New"
    }
    buildingCondition = st.selectbox(
        "Building Condition",
        options=list(building_condition_options.keys()),
        format_func=lambda x: building_condition_options[x],
        index=2
    )

    has_garden_options = {1: "Yes", 0: "No"}
    hasGarden = st.selectbox(
        "Has Garden?",
        options=list(has_garden_options.keys()),
        format_func=lambda x: has_garden_options[x],
        index=1
    )

    gardenSurface = st.number_input("Garden Surface (int)", value=100)

    has_terrace_options = {1: "Yes", 0: "No"}
    hasTerrace = st.selectbox(
        "Has Terrace?",
        options=list(has_terrace_options.keys()),
        format_func=lambda x: has_terrace_options[x],
        index=1
    )

    epc_score_options = {
        9: "A++",
        8: "A+",
        7: "A",
        6: "B",
        5: "C",
        4: "D",
        3: "E",
        2: "F",
        1: "G"
    }
    epcScore = st.selectbox(
        "EPC Score",
        options=list(epc_score_options.keys()),
        format_func=lambda x: f"{x} - {epc_score_options[x]}",
        index=5
    )

    has_parking_options = {1: "Yes", 0: "No"}
    hasParking = st.selectbox(
        "Has Parking?",
        options=list(has_parking_options.keys()),
        format_func=lambda x: has_parking_options[x],
        index=1
    )

    postCode = st.number_input("Post Code (int)", value=1050, step=1)
    type_ = st.text_input("Type (string)", value="House")
    province = st.text_input("Province (string)", value="Brussels")
    subtype = st.text_input("Subtype (string)", value="House")
    region = st.text_input("Region (string)", value="Brussels-Capital")

    submit = st.form_submit_button("Predict")

if submit:
    data = {
        "habitableSurface": habitableSurface,
        "bedroomCount": bedroomCount,
        "buildingCondition": buildingCondition,
        "hasGarden": hasGarden,
        "gardenSurface": gardenSurface,
        "hasTerrace": hasTerrace,
        "epcScore": epcScore,
        "hasParking": hasParking,
        "postCode": postCode,
        "type": type_,
        "province": province,
        "subtype": subtype,
        "region": region
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            prediction = response.json().get("predictions")
            formatted_price = f"€ {prediction:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.success(f"Predicted price: {formatted_price}")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
