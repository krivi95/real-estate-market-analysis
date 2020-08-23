"""Python file containing various sql statements for initializing database and storing content into it."""

class SqlStatements:
    """Class containing SQL statements for working with PostgreSQL database, for web scraping purposes in ."""  

    @staticmethod
    def database_exists(db_name):
        return f"SELECT EXISTS(SELECT FROM pg_catalog.pg_database where datname='{db_name}')"

    @staticmethod
    def create_database(db_name, user):
        return f"""
            CREATE DATABASE {db_name}
            WITH 
            OWNER = {user}
            ENCODING = 'UTF8'
            CONNECTION LIMIT = -1;
            """

    @staticmethod
    def create_properies_table():
        return """
            CREATE TABLE IF NOT EXISTS properties
            (
                id serial  PRIMARY KEY,   
                listing_type "char",
                property_type "char",
                price real,
                location_city text,
                location_city_district text,
                area_property real,
                area_land real,
                construction_type text,
                num_floors_building integer,
                apartment_floor real,
                registered boolean,
                heating_type text,
                num_rooms real,
                num_bathrooms integer,
                source text         
            );
            """

    @staticmethod
    def insert_new_real_estate():
        return """
            INSERT INTO properties(
                       listing_type,
                       property_type, 
					   price, 
					   location_city, 
					   location_city_district, 
					   area_property,
                       area_land,
					   construction_type,
					   num_floors_building,
					   apartment_floor,
					   registered,
					   heating_type,
					   num_rooms,
                       num_bathrooms,
					   source)
		 	values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    
    @staticmethod
    def insert_apartment():
        return """
            INSERT INTO properties(
                       listing_type,
                       property_type, 
					   price, 
					   location_city, 
					   location_city_district, 
					   location_lat, 
					   location_long, 
					   area_property,
					   construction_type,
					   num_floors_building,
					   apartment_floor,
					   registered,
					   heating_type,
					   num_rooms,
					   source)
		 	values('s', 'a', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """