# Standard library imports
import os
from enum import Enum

# Third party libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle

LINEAR_REGRESSION_DIR = r'models\linear_regression_model'
LINEAR_REGRESSION_WEIGHTS = 'weights.txt'
LINEAR_REGRESSION_ENCODER = 'onehotencoder.pickle'
LINEAR_REGRESSION_SCALER = 'standardizer.pickle'

class ML_MODEL(Enum):
    LINEAR_REGRESSION = 'Multiple linear regression'
    CLASSIFICATION = 'Classification (SVM)'

class CITY_DISTRICT(Enum):
    STARI_GRAD = 'Stari grad'
    ZVEZDARA = 'Zvezdara'
    VRACAR = 'Vracar'
    PALILULA = 'Palilula'
    NOVI_BEOGRAD = 'Novi Beograd'   
    CUKARICA = 'Cukarica' 
    SAVSKI_VENAC = 'Savski Venac'
    ZEMUN = 'Zemun'
    RAKOVICA = 'Rakovica'
    VOZDOVAC = 'Vozdovac'
    MLADENOVAC = 'Mladenovac'
    GROCKA = 'Grocka'
    LAZAREVAC = 'Lazarevac'
    OBRENOVAC = 'Obrenovac'
    SURCIN = 'Surcin'
    BARAJEVO = 'Barajevo'

class HEATING_TYPE(Enum):
    CENTRALNO = 'Centralno'
    ETAZNO = 'Etažno'
    GAS = 'Gas'
    KALJEVA_PEC = 'Kaljeva peć'
    NORVESKI_RADIJATORI = 'Norveški radijatori'
    PODNO = 'Podno'
    STRUJA = 'Struja'
    TA_PEC = 'TA peć'

def get_features_dataframe_template():
    return pd.DataFrame(columns=['location_city_district', 'area_property', 'registered', 'heating_type', 'num_rooms'])

def populate_template_with_features(location_city_district, area_property, registered, heating_type, num_rooms):
    template = get_features_dataframe_template()
    template = template.append({
        'location_city_district': location_city_district, 
        'area_property': area_property,
        'registered': registered, 
        'heating_type': heating_type, 
        'num_rooms': num_rooms
        },
        ignore_index=True)
    return template 


# Main title
st.title('Belgrade real estate')

# User selected model from sidebar 
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in ML_MODEL])

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

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
data = populate_template_with_features(location_city_district, area_property, registered, heating_type, num_rooms)

@st.cache
def import_coefficients(path):
    coefficients = []
    with open(path, 'r') as input_file:
        for line in input_file:
            coefficients.append(float(line))
    return coefficients  

@st.cache
def unpickle_encoder(path):
    encoder = None
    with open(path, 'rb') as input_file:
        encoder = pickle.load(input_file)
    return encoder  

@st.cache
def unpickle_scaler(path):
    scaler = None
    with open(path, 'rb') as input_file:
        scaler = pickle.load(input_file)
    return scaler  

def predict(w, x):
        """
        Calculates multiple linear regression hyposthesis based on the current weights in regression class.
        Hypothesis: W1*X1 + W2*X2 + ... + Wn*Xn + W0
        """
        # W0 is the last element in weights array
        x = x.reshape(27,-1)
        y = w[-1] 
        for i in range(len(x)):
            y+= x[i] * w[i]
        return y

if pricing_method == ML_MODEL.LINEAR_REGRESSION.value and st.button(f'Predict the real estate price'):
    # Importing multiple regression coefficients
    coefficients = import_coefficients(os.path.join(LINEAR_REGRESSION_DIR, LINEAR_REGRESSION_WEIGHTS))

    # Deserializing OneHotEncoder encoder
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    encoder = unpickle_encoder(os.path.join(LINEAR_REGRESSION_DIR, LINEAR_REGRESSION_ENCODER))
    
    # Deserializing StandardScaler
    from sklearn.preprocessing import StandardScaler
    scaler = unpickle_scaler(os.path.join(LINEAR_REGRESSION_DIR, LINEAR_REGRESSION_SCALER))
    
    # Encoding categorical variables
    data = np.array(encoder.transform(data))
    
    # Scaling numerical variables
    data = scaler.transform(data)

    # Creating a prediction
    prediction = predict(coefficients, data)
    st.subheader(f'Predicted price for described flat in Belgrade is : {round(prediction[0], 2)} €.')