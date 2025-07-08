import streamlit as st
import requests

API_URL = 'https://immoeliza-api-66pt.onrender.com/'

st.title("ImmoEliza Price Prediction")

# Input form
with st.form("prediction_form"):
    habitableSurface = st.number_input("Habitable Surface (float)", value=120.5)
    bedroomCount = st.number_input("Bedroom Count (int)", value=3, step=1)
    buildingCondition = st.number_input("Building Condition (int)", value=4, step=1)
    hasGarden = st.selectbox("Has Garden?", options=[0, 1])
    gardenSurface = st.number_input("Garden Surface (float)", value=50.0)
    hasTerrace = st.selectbox("Has Terrace?", options=[0, 1])
    epcScore = st.number_input("EPC Score (float)", value=180.0)
    hasParking = st.selectbox("Has Parking?", options=[0, 1])
    postCode = st.number_input("Post Code (int)", value=1000, step=1)
    type_ = st.text_input("Type (string)", value="Apartment")
    province = st.text_input("Province (string)", value="Brussels")
    subtype = st.text_input("Subtype (string)", value="Penthouse")
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
            st.success(f"Predicted price: {prediction}")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")