import MySQLdb
import MySQLdb.cursors
from flask import current_app as app

"""
Database Connection Class

Working with MySQLdb.
Class that establishes connection(Instance) to the Database.
Creates attributes and methods to allow interaction with Database
"""

# Connection Object
class DBConnection:
    def __init__(self):
        #Initial DB Connection
        self.db_connection = MySQLdb.connect(host=app.config['DB_HOST'],
                                            port=app.config['DB_PORT'],
                                            user=app.config['DB_USER'],
                                            passwd=app.config['DB_PASS'],
                                            db=app.config['DB_NAME'],
                                            cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.db_connection.cursor()

    #Refresh Method: Closes and Restablishes Connection
    def update(self):
        self.close()
        self.db_connection = MySQLdb.connect(host=app.config['DB_HOST'],
                                            port=app.config['DB_PORT'],
                                            user=app.config['DB_USER'],
                                            passwd=app.config['DB_PASS'],
                                            db=app.config['DB_NAME'],
                                            cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.db_connection.cursor()

    #Query Method: Allows us to use the Cursor Object to run Queries to the DB
    def query(self, query: str, values: list):
        self.update()
        self.cursor.execute(query, values)
        query_results = self.cursor.fetchall()
        return query_results

    #Commits all Changes to the DB and Updates the DB Connection
    def save(self):
        self.db_connection.commit()
        self.update()

    #Closes the Current DB Connection
    def close(self):
        self.db_connection.close()