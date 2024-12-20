import streamlit as st
import requests
import pandas as pd

# Set API endpoint
API_URL = "http://159.65.164.99"  # Your DigitalOcean droplet IP

# Set page configuration
st.set_page_config(
    page_title="Mental Health Treatment Prediction",
    page_icon="🧠",
    layout="centered"
)

# Title and description
st.title("Mental Health Treatment Prediction")
st.markdown("""
This app predicts whether someone is likely to seek mental health treatment based on various factors.
Please fill in the details below to get a prediction.
""")

# Create input form
with st.form("prediction_form"):
    st.subheader("Personal Information")
    
    # Age input
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    
    # Gender selection
    gender = st.selectbox(
        "Gender",
        options=["male", "female", "other"]
    )
    
    # Country input
    country = st.selectbox(
        "Country",
        options=["United States", "United Kingdom", "Canada", "Germany", "Other"]
    )
    
    st.subheader("Employment Information")
    
    # Company size
    company_size = st.selectbox(
        "Company Size",
        options=["1-25", "26-100", "100-500", "500-1000", "1000+"]
    )
    
    # Tech company
    is_tech_company = st.radio(
        "Is your employer primarily a tech company?",
        options=["Yes", "No"],
        horizontal=True
    )
    
    # Remote work
    work_remotely = st.selectbox(
        "Work Arrangement",
        options=["never", "sometimes", "always"]
    )
    
    st.subheader("Mental Health Benefits")
    
    # Mental health benefits
    has_mental_health_benefits = st.radio(
        "Does your employer provide mental health benefits?",
        options=["yes", "no", "not sure"],
        horizontal=True
    )
    
    # Current mental health condition
    current_disorder = st.radio(
        "Do you currently have a mental health condition?",
        options=["yes", "no", "not sure"],
        horizontal=True
    )
    
    # Submit button
    submitted = st.form_submit_button("Predict")

# Make prediction when form is submitted
if submitted:
    # Prepare data for API
    data = {
        "age": age,
        "gender": gender,
        "country": country,
        "company_size": company_size,
        "is_tech_company": 1 if is_tech_company == "Yes" else 0,
        "work_remotely": work_remotely,
        "has_mental_health_benefits": has_mental_health_benefits,
        "current_disorder": current_disorder
    }
    
    try:
        # Make API request
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            prediction = response.json()
            
            # Display prediction
            st.subheader("Prediction Results")
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Probability",
                    value=f"{prediction['probability']:.1%}"
                )
            
            with col2:
                st.metric(
                    label="Prediction",
                    value=prediction['prediction']
                )
            
            # Additional information
            st.info("""
            📊 Interpretation:
            - Probability shows the model's confidence in its prediction
            - A higher percentage indicates stronger likelihood of seeking treatment
            """)
        else:
            st.error(f"Error from API: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Error connecting to the API. Please check if the service is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add footer with information
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🧠 Mental Health Treatment Prediction App</p>
    <p>Created with Streamlit & FastAPI</p>
</div>
""", unsafe_allow_html=True)

