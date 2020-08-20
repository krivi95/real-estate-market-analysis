# Standard library import
import json

# Third party import
import psycopg2

# Local import
from sql_statements import SqlStatements

class Connection:
    """
    Connection class handles datase creation, initialization, connections (opening, colosing).
    """

    def __init__(self, connection_parameters):
        """Recieves parameters for establishing connection in JSON format."""
        self.connection_parameters = connection_parameters
        self.open_connections = []
        self.num_connections = 0

    def open_connection(self):
        """
        Opens new connection and remembers it internally.
        If specified database in parametes doesn't exist, it creates new database.
        """
        host = self.connection_parameters['host']
        port = self.connection_parameters['port']
        user = self.connection_parameters['user']
        password = self.connection_parameters['password']
        database = self.connection_parameters['database']
        
        if not self._database_exists(host, port, database, user, password):
            # If database doesn't exist on the specified server, create a new db.
            self._initialize_database(host, port, database, user, password)

        # Create and save new connection to db
        conn = self._connect(host, port, database, user, password)
        if conn is not None:
            self.open_connections.append(conn)
        return conn

    def close_connection(self, conn):
        """Closes previously established connection by this class."""
        try:
            if conn is not None and conn in self.open_connection:
                self.open_connection.remove(conn)
                conn.close()
                print('Database connection closed.')
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def _connect(self, host, port, database, user, password):
        """Establishes new connection to dabase with provided parameters."""
        try:
            conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
            return conn
        except Exception as e:
            print(e)
            return None

    def _database_exists(self, host, port, database, user, password):
        """Checks if specified database already exists on server.""" 
        try:
            conn = psycopg2.connect(host=host, port=port, user=user, password=password)
            with conn.cursor() as curr: 
                query = SqlStatements.database_exists(database)
                curr.execute(query)
                return curr.fetchone()[0] 
        except Exception as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()

    def _initialize_database(self, host, port, database, user, password):
        """If database doesn't exist on the server creates new databse from specified paramers."""
        try:
            # Creating new database
            conn = psycopg2.connect(host=host, port=port, user=user, password=password)
            conn.set_session(autocommit=True)
            with conn.cursor() as curr:
                query = SqlStatements.create_database(database, user)
                curr.execute(query)
                print(f'Database {database} created.')
            conn.commit()
            conn.close()
            
            # Creating new table for storing property listings from web
            conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
            conn.set_session(autocommit=True)
            with conn.cursor() as curr:
                query = SqlStatements.create_properies_table()
                curr.execute(query)
                print(f'Table properties created.')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    with open('db_connetion.json') as db_file:

        parameters = json.load(db_file)
        connection_utils = Connection(parameters)
        connection_utils.open_connection()