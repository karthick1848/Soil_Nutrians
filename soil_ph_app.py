import streamlit as st
import pickle
import pandas as pd

# Load the model and feature columns
with open('soil_ph_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('feature_columns.pkl', 'rb') as file:
    feature_columns = pickle.load(file)

# Streamlit app
st.title('Soil pH Prediction')
st.write("""
This app predicts soil pH based on soil composition and organic matter content.
""")

# Sidebar with user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    sand = st.sidebar.slider('Sand %', 0.0, 100.0, 40.0)
    clay = st.sidebar.slider('Clay %', 0.0, 100.0, 30.0)
    silt = st.sidebar.slider('Silt %', 0.0, 100.0, 30.0)
    om = st.sidebar.slider('Organic Matter %', 0.0, 10.0, 2.0)
    
    # Ensure the percentages add up to 100
    total = sand + clay + silt
    if total != 100:
        st.sidebar.warning(f"Percentages add up to {total}%. Please adjust to total 100%.")
    
    data = {
        'Sand %': sand,
        'Clay %': clay,
        'Silt %': silt,
        'O.M. %': om
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display user input
st.subheader('User Input Parameters')
st.write(input_df)

# Make prediction
prediction = model.predict(input_df)

st.subheader('Prediction')
st.write(f"Predicted Soil pH: {prediction[0]:.2f}")

# Model coefficients
st.subheader('Model Coefficients')
coefficients = pd.DataFrame({
    'Feature': feature_columns,
    'Coefficient': model.coef_
})
st.write(coefficients)

st.write("""
### Interpretation
- Positive coefficients indicate that as the feature increases, pH tends to increase
- Negative coefficients indicate that as the feature increases, pH tends to decrease
""")
