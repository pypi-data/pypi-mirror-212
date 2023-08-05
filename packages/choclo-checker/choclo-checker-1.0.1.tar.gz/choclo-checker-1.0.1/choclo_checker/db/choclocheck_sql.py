"""
ChocloChecker SQL Module

This module contains the functions for executing SQL queries and checking the status of SQL databases.
"""

import pyodbc

def check_connection(driver, server, database, username, password):
    """
    Check the connection to the SQL server.

    Args:
        driver (str): The driver name for the SQL server.
        server (str): The server address of the SQL server.
        database (str): The name of the SQL database.
        username (str): The username for SQL authentication.
        password (str): The password for SQL authentication.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(conn_str)
        conn.close()
        return True
    except pyodbc.OperationalError:
        return False

def execute_query(driver, server, database, username, password, query):
    """
    Execute an SQL query on the SQL server.

    Args:
        driver (str): The driver name for the SQL server.
        server (str): The server address of the SQL server.
        database (str): The name of the SQL database.
        username (str): The username for SQL authentication.
        password (str): The password for SQL authentication.
        query (str): The SQL query to execute.

    Returns:
        list: A list of dictionaries containing the query results.
    """
    try:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return results
    except pyodbc.OperationalError:
        return []

def check_sql(driver, server, database, username, password, query=None):
    """
    Check the status of an SQL database.

    Args:
        driver (str): The driver name for the SQL server.
        server (str): The server address of the SQL server.
        database (str): The name of the SQL database.
        username (str): The username for SQL authentication.
        password (str): The password for SQL authentication.
        query (str, optional): The SQL query to execute.

    Returns:
        dict: A dictionary containing the status of the SQL database.
            The dictionary includes the connection status, database status,
            and the results of the specified query (if provided).
    """
    status = {}

    status["connection"] = check_connection(driver, server, database, username, password)
    status["database"] = "Running and accessible" if status["connection"] else "Cannot connect to the database"
    if query:
        status["query_results"] = execute_query(driver, server, database, username, password, query)

    return status
