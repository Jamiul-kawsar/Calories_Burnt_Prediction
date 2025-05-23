import streamlit as st
import pickle

# Load the model
model = pickle.load(open('calories_model.pkl', 'rb'))

# Application title
st.title('Calories Burnt Prediction')
st.write('This app predicts the calories burnt based on your input parameters.')
st.write('Please enter the following details to get your prediction:')  

# Input fields for user data
gender = st.selectbox("Gender", ["Male", "Female"])
gender_value = 1 if gender == "Male" else 0

age = st.number_input("Age", min_value = 1, max_value = 120, value = 20)
height = st.number_input("Height (cm)", min_value = 50, max_value = 250, value = 165)
