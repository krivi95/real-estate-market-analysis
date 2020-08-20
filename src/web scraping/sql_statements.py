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
                city "char"[],
                city_district "char"[],
                area_property real,
                year_construction smallint,
                area_land real,
                building_floors integer,
                apartment_floor integer,
                registered boolean,
                heating_type "char"[],
                rooms integer,
                bathrooms integer,
                source "char"[],
                source_id "char"[]           
            );
            """