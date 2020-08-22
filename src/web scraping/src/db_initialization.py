# Standard library import
import json

# Local package import
from realestate.realestate.db_connection.connection import Connection


if __name__ == "__main__":
    with open('db_connetion.json') as db_file:
        # Loading db connection parameters 
        parameters = json.load(db_file)

        # Opening db connection and creating db and tables in firs run
        connection_utils = Connection(parameters)
        conn = connection_utils.open_connection()

        # Closing connection        
        connection_utils.close_connection(conn)