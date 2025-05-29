import streamlit as st
import pickle
import numpy as np

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
        with open("calories_model.pkl", "rb") as f:
            model = pickle.load(f)
            return model
    except FileNotFoundError:
        st.error("Model file 'calories_model.pkl' not found. Please ensure the model file is in the correct directory.")
        return None

model = load_model()

#webpage style CSS

st.markdown("""
<style> 
    /* General body styles */      
    /* Sidebar Background Color */
    section[data-testid="stSidebar"] {
        background: #000000;
        border-right: 3px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #8B0000 !important;
        color: white !important;
        border: none;
        border-radius: 6px;
        padding: 0.5em 1em;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #A30000 !important;
    }
    .main-header {
        background: #0095cc; 
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: #0095cc;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #007bb5;/* Darker blue on hover */
        color: white;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: none;
    }
    .input-section {
        background: #000000;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
    st.markdown('<div class = "input-section">', unsafe_allow_html=True)
    st.subheader("📊 Personal Information")

    # create two sub-columns 
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        gender = st.selectbox("👤 Gender", ["Male", "Female"])
        age = st.number_input("🎂 Age", min_value = 1, max_value = 120, value = 25, step = 1)
        height = st.number_input("📏 Height (cm)", min_value = 50, max_value = 250, value = 170, step = 1)
        weight = st.number_input("⚖️ Weight (kg)", min_value = 20, max_value = 200, value = 70, step = 1)
    with input_col2:
        duration = st.number_input("⏱️ Duration (minutes)", min_value = 1, max_value = 300, value = 30, step = 1)
        heart_rate = st.number_input("❤️ Heart Rate (bpm)", min_value = 40, max_value = 200, value = 100, step = 1)
        body_temp = st.number_input("🌡️ Body Temperature (°C)", min_value = 30.0, max_value = 45.0, value = 37.0, step = 0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # prediction button
    predict_button = st.button("🔥 Predict Calories Burnt", type="primary")
with col2:
    st.subheader("📈 Prediction Results")

    if predict_button:
        # Convert gender to numeric
        gender_value = 1 if gender == "Male" else 0

        input_data = np.array([[gender_value, age, height, weight, duration, heart_rate, body_temp]])
        colmn1, colmn2 = st.columns(2)

        # Make prediction
        with st.spinner("Calculating..."):
            prediction = model.predict(input_data)[0]
            #st.success(f"🔥 Predicted Calories Burnt: **{prediction:.2f} kcal**")
        
            # Display results with custom styling
        st.markdown(f"""
        <div class="prediction-card" >
            <h2>🔥 {prediction:.1f} kcal</h2>
            <p>Estimated Calories Burnt</p>
        </div>
        """, unsafe_allow_html=True)

        with colmn1:    
            #additional insights
            st.markdown("📊 Additional Insights")

            #calculate calories burnt per minute
            calories_per_minute = prediction / duration if duration > 0 else 0
            st.metric("Calories Burnt per Minute", f"{calories_per_minute:.2f} kcal/min")

        with colmn2:
            #calculate BMI 
            bmi = weight / ((height / 100) ** 2)
            st.metric("Body Mass Index (BMI)", f"{bmi:.2f}")

            # BMI category
            if bmi < 18.5:
                bmi_category = "Underweight"
                color = "blue"
            elif 18.5 <= bmi < 24.9:
                bmi_category = "Normal weight"
                color = "green"
            elif 25 <= bmi < 29.9:
                bmi_category = "Overweight"
                color = "orange"
            else:
                bmi_category = "Obesity"
                color = "red"
            # display BMI category with color
            st.markdown(f"**BMI Category:** :{color}[{bmi_category}]")

            # intensity level based on heart rate
            if heart_rate < 100:
                intensity = "Low"
                color = "green"
            elif heart_rate < 150:
                intensity = "Moderate"
                color = "orange"
            else:
                intensity = "High"
                color = "red"
            st.markdown(f"**Exercise Intensity:** :{color}[{intensity}]")
        
        # Success message
        st.success("✅ Prediction completed successfully!")
    else:
        st.info("👆 Enter your details and click 'Predict' to see results")

# Additional information section accuracy tips etc.
st.markdown("---")
st.subheader("ℹ️ About the Prediction Model")

info_col1, info_col2, info_col3 = st.columns(3)
with info_col1:
     st.markdown("""
    **🎯 Accuracy**
    - Based on machine learning model
    - Trained on real fitness data
    - Considers multiple factors
    """)
     
with info_col2:
    st.markdown("""
    **📋 Input Factors**
    - Personal characteristics
    - Exercise duration
    - Heart rate during activity
    - Body temperature
    """)

with info_col3:
    st.markdown("""
    **💡 Tips**
    - Ensure accurate heart rate
    - Use consistent measurements
    - Consider individual variations
    """)

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
    """)

    st.markdown("---")

    st.markdown("""
    ### 📚 Resources
    - [Understanding Calories Burnt](https://www.healthline.com/nutrition/how-many-calories-burned)
    - [Fitness and Nutrition Guide](https://www.choosemyplate.gov/)
    """)
    st.markdown("---")

    st.markdown("""
    ### 🛠️ Developer
    - [Jamiul Kawsar](https://github.com/Jamiul-kawsar)
    - [GitHub Repository](https://github.com/Jamiul-kawsar/Calories_Burnt_Prediction)
    """)
    st.markdown("---")
    # reset button
    if st.button("🔄 Reset All Values"):
        st.session_state.clear()
        st.rerun()
    
# footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔥 Calories Burnt Predictor | Built with Streamlit</p>
    <p>Made by <a href="https://github.com/Jamiul-kawsar">Jamiul Kawsar</a></p>
</div>
""", unsafe_allow_html=True)
