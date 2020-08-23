# Standard library imports
from enum import Enum


class FLOOR_TYPE(Enum):
    PODRUM = ('podrum', -1)
    SUTEREN = ('suteren', -1)
    NISKO_PRIZEMLJE = ('niskoprizemlje', 0)
    PRIZEMLJE = ('prizemlje', 0)
    VISOKO_PRIZEMLJE = ('visokoprizemlje', 0.5)
    POTKROVLJE = ('potkrovlje', 100)

class RealEstateUtils():

    @staticmethod
    def get_property_dictionary():
        property_dictionary = {       
            'listing_type': None,
            'property_type': None, 
            'price': None, 
            'location_city': None, 
            'location_city_district': None, 
            'area_property': None,
            'area_land': None,
            'construction_type': None,
            'num_floors_building': None,
            'apartment_floor': None,
            'registered': None,
            'heating_type': None,
            'num_rooms': None,
            'num_bathrooms': None,
            'source': None
        }
        return property_dictionary
    
    @staticmethod
    def calculate_floor_value_based_on_type(floor):
        for floor_type in FLOOR_TYPE:
            if floor_type.value[0] == floor:
                return floor_type.value[1]
        return -100

if __name__ == "__main__":
    a = RealEstateUtils.calculate_floor_value_based_on_type('pridzemlje')
    print(a)