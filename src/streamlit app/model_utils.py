import pickle
import streamlit as st
import pandas as pd


@st.cache
def import_coefficients(path):
    coefficients = []
    with open(path, 'r') as input_file:
        for line in input_file:
            coefficients.append(float(line))
    return coefficients  

@st.cache
def unpickle_svm_model(path):
    svm = None
    with open(path, 'rb') as input_file:
        svm = pickle.load(input_file)
    return svm  

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

def get_features_dataframe_template_for_classification():
    return pd.DataFrame(columns=[
        'location_city_district', 
        'area_property', 
        'num_floors_building', 
        'apartment_floor', 
        'registered', 
        'heating_type', 
        'num_rooms',
        'num_bathrooms'
        ])

def populate_template_with_features_for_classification(location_city_district, area_property, num_floors_building, 
                                                        apartment_floor, registered, heating_type, num_rooms, num_bathrooms):
    template = get_features_dataframe_template_for_classification()
    template = template.append({
        'location_city_district': location_city_district, 
        'area_property': area_property,
        'num_floors_building': num_floors_building, 
        'apartment_floor': apartment_floor,
        'registered': registered, 
        'heating_type': heating_type, 
        'num_rooms': num_rooms,
        'num_bathrooms': num_bathrooms
        },
        ignore_index=True)
    return template 

def get_features_dataframe_template_for_regression():
    return pd.DataFrame(columns=[
        'location_city_district', 
        'area_property', 
        'registered', 
        'heating_type', 
        'num_rooms'
        ])

def populate_template_with_features_for_regression(location_city_district, area_property, registered, heating_type, num_rooms):
    template = get_features_dataframe_template_for_regression()
    template = template.append({
        'location_city_district': location_city_district, 
        'area_property': area_property,
        'registered': registered, 
        'heating_type': heating_type, 
        'num_rooms': num_rooms
        },
        ignore_index=True)
    return template 

def regressor_predict(w, x):
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

def map_class_to_category(category):
    if category == 0:
        return "less than 50.000 €"
    elif category == 1:
        return " 50.000 - 100000 €"
    elif category == 2:
        return "100.000 - 150.000 €"
    elif category == 3:
        return "150.000 - 200.000 €"
    elif category == 4:
        return "greated than 200.000 €"
    else:
        return "Wasn't able to determine the price category."
