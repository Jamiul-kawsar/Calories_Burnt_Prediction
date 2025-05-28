import streamlit as st
import pickle

# page configuration
st.set_page_config(
    page_title = "Calories Burnt Predictor",
    page_icon = "🔥",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Load the model
@st.cache_resource
def load_model():
    try: 
        model = pickle.load(open('calories_model.pkl', 'rb'))
        return model
    except FileNotFoundError:
        st.error("Model file 'calories_model.pkl' not found. Please ensure the model file is in the correct directory.")
        return None

model = load_model()

#webpage style

# header
st.markdown("""
<div class = "main-header">
    <h1>🔥 Calories Burnt Predictor</h1>
    <p>Get accurate predictions based on your personal data and activity data</p>
</div>
""", unsafe_allow_html = True)

 # Stop execution if model is not loaded
if model is None:
    st.stop()

