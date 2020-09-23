# Standard library imports
import os

# Third party libraries
import streamlit as st
import pandas as pd
import numpy as np

# Lokal project imports
import svm
from settings import (
    ML_MODEL, 
    CITY_DISTRICT, 
    HEATING_TYPE, 
    REGRESSION_SETTINGS,
    CLASSIFICATION_SETTINGS
)
from model_utils import(
    import_coefficients,
    unpickle_svm_model,
    unpickle_encoder,
    unpickle_scaler,
    regressor_predict,
    map_class_to_category,
    populate_template_with_features_for_regression,
    populate_template_with_features_for_classification
)
 

# Main title
st.title('Belgrade real estate')

# User selected model from sidebar 
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in ML_MODEL])

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

if pricing_method == ML_MODEL.LINEAR_REGRESSION.value:
    #Linear regression has been selected.

    # Input fields (model features)
    location_city_district = st.selectbox(
        'City district:',
        sorted([district.value for district in CITY_DISTRICT])
        ).lower()
    area_property = st.number_input('Flat size (m2):', min_value=0, value=65)
    num_rooms = st.number_input('Number of rooms:', min_value=0, value=2)
    heating_type = st.selectbox(
        'Heating type:',
        sorted([district.value for district in HEATING_TYPE])
        )
    registered = st.selectbox(
        'Registered:',
        [True, False]
        )

    # Selected data
    data = populate_template_with_features_for_regression(location_city_district, area_property, registered, heating_type, num_rooms)

    if st.button(f'Predict the real estate price'):
        #Making pridicting using linear regression.

        # Importing multiple regression coefficients
        coefficients = import_coefficients(os.path.join(REGRESSION_SETTINGS.BACKUP_DIRECTORY.value, REGRESSION_SETTINGS.WEIGHTS.value))

        # Deserializing OneHotEncoder encoder
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        encoder = unpickle_encoder(os.path.join(REGRESSION_SETTINGS.BACKUP_DIRECTORY.value, REGRESSION_SETTINGS.ENCODER.value))
        
        # Deserializing StandardScaler
        from sklearn.preprocessing import StandardScaler
        scaler = unpickle_scaler(os.path.join(REGRESSION_SETTINGS.BACKUP_DIRECTORY.value, REGRESSION_SETTINGS.SCALER.value))
        
        # Encoding categorical variables
        data = np.array(encoder.transform(data))
        
        # Scaling numerical variables
        data = scaler.transform(data)

        # Creating a prediction
        prediction = regressor_predict(coefficients, data)
        st.subheader(f'Predicted price for described flat in Belgrade is : {round(prediction[0], 2)} €.')

elif pricing_method == ML_MODEL.CLASSIFICATION.value:
    #Classification regression has been selected.

    # Input fields (model features)
    location_city_district = st.selectbox(
        'City district:',
        sorted([district.value for district in CITY_DISTRICT])
        ).lower()
    area_property = st.number_input('Flat size (m2):', min_value=0, value=65)
    num_rooms = st.number_input('Number of rooms:', min_value=0, value=2)
    num_bathrooms = st.number_input('Number of bathrooms:', min_value=0, value=2)
    heating_type = st.selectbox(
        'Heating type:',
        sorted([district.value for district in HEATING_TYPE])
        )
    registered = st.selectbox(
        'Registered:',
        [True, False]
        )
    apartment_floor = st.number_input('Apartment floor:', min_value=-1, max_value=40, value=5)
    num_floors_building = st.number_input('Number of foors in the building:', min_value=0, max_value=40, value=7)

    # Selected data
    data = populate_template_with_features_for_classification(
        location_city_district, area_property, num_floors_building, 
        apartment_floor, registered, heating_type, num_rooms, num_bathrooms
        )
    
    if st.button(f'Predict the real estate price segment'):
        #Making classification using kernel svm.
        
        # Importing classification model
        svm_model = unpickle_svm_model(os.path.join(CLASSIFICATION_SETTINGS.BACKUP_DIRECTORY.value, CLASSIFICATION_SETTINGS.MODEL.value))

        # Deserializing OneHotEncoder encoder
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        encoder = unpickle_encoder(os.path.join(CLASSIFICATION_SETTINGS.BACKUP_DIRECTORY.value, CLASSIFICATION_SETTINGS.ENCODER.value))
        
        # Deserializing StandardScaler
        from sklearn.preprocessing import StandardScaler
        scaler = unpickle_scaler(os.path.join(CLASSIFICATION_SETTINGS.BACKUP_DIRECTORY.value, CLASSIFICATION_SETTINGS.SCALER.value))
        
        # Encoding categorical variables
        data = np.array(encoder.transform(data))
        
        # Scaling numerical variables
        data = scaler.transform(data)

        # Creating a prediction
        prediction = svm_model.predict(data)
        st.subheader('Predicted price segment for described flat in Belgrade is :')
        st.subheader(f'{map_class_to_category(prediction[0])}')
        
    
    
    