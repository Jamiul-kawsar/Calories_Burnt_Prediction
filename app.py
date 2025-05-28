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

#create two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class = "input-header">', unsafe_allow_html=True)
    st.subheader("📊 Personal Information")

    # create two sub-columns 
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        gender = st.selectbox("👤 Gender", ["Male", "Female"])
        age = st.number_input("🎂 Age", min_value = 1, max_value = 120, value = 25, step = 1)


#sidebar for additional information
with st.sidebar:
    st.header("ℹ️ App Information")
    st.markdown("""
    ### How it works?
    1. Enter your personal information
    2. Input exercise data
    3. Get your calorie burn prediction
    4. View additional insights
    """)
    st.markdown("---")

    st.markdown("""
    ### 📊 Input Ranges:
    - **Age:** 1-120 years
    - **Height:** 50-250 cm
    - **Weight:** 20-200 kg
    - **Duration:** 1-300 minutes
    - **Heart Rate:** 40-200 bpm
    - **Body Temp:** 30-45°C
    - **Speed:** 0-30 km/h
    """)

