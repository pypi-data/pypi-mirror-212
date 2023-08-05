"""
ChocloChecker PostgreSQL Module

This module contains the functions for monitoring the status of PostgreSQL databases.
"""

import psycopg2

def check_connection(host, port, username, password, database):
    """
    Check the connection to the PostgreSQL server.

    Args:
        host (str): The host address of the PostgreSQL server.
        port (int): The port number of the PostgreSQL server.
        username (str): The username for PostgreSQL authentication.
        password (str): The password for PostgreSQL authentication.
        database (str): The name of the PostgreSQL database.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        conn = psycopg2.connect(host=host, port=port, user=username, password=password, dbname=database)
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False

def check_status(host, port, username, password, database):
    """
    Check the status of the PostgreSQL database.

    Args:
        host (str): The host address of the PostgreSQL server.
        port (int): The port number of the PostgreSQL server.
        username (str): The username for PostgreSQL authentication.
        password (str): The password for PostgreSQL authentication.
        database (str): The name of the PostgreSQL database.

    Returns:
        str: The status of the PostgreSQL database.
    """
    connection_status = check_connection(host, port, username, password, database)
    if connection_status:
        return "Database is running and accessible"
    else:
        return "Cannot connect to the database"

def check_tablespace(host, port, username, password, database, tablespace):
    """
    Check the status of a specific tablespace in the PostgreSQL database.

    Args:
        host (str): The host address of the PostgreSQL server.
        port (int): The port number of the PostgreSQL server.
        username (str): The username for PostgreSQL authentication.
        password (str): The password for PostgreSQL authentication.
        database (str): The name of the PostgreSQL database.
        tablespace (str): The name of the tablespace to check.

    Returns:
        dict: A dictionary containing the status of the specified tablespace.
            The dictionary includes values such as total space, used space, and free space.
    """
    try:
        conn = psycopg2.connect(host=host, port=port, user=username, password=password, dbname=database)
        cursor = conn.cursor()

        query = f"SELECT tablespace_name, pg_size_pretty(pg_tablespace_size('{tablespace}')) " \
                f"FROM pg_tablespace WHERE tablespace_name = '{tablespace}'"
        cursor.execute(query)
        result = cursor.fetchone()

        tablespace_status = {
            "tablespace": result[0],
            "size": result[1]
        }

        cursor.close()
        conn.close()

        return tablespace_status
    except psycopg2.OperationalError:
        return {}

def check_postgres(host, port, username, password, database, tablespace=None):
    """
    Check the status of a PostgreSQL database.

    Args:
        host (str): The host address of the PostgreSQL server.
        port (int): The port number of the PostgreSQL server.
        username (str): The username for PostgreSQL authentication.
        password (str): The password for PostgreSQL authentication.
        database (str): The name of the PostgreSQL database.
        tablespace (str, optional): The name of the tablespace to check.

    Returns:
        dict: A dictionary containing the status of the PostgreSQL database.
            The dictionary includes the connection status, database status,
            and the status of the specified tablespace (if provided).
    """
    status = {}

    status["connection"] = check_connection(host, port, username, password, database)
    status["database"] = check_status(host, port, username, password, database)
    if tablespace:
        status["tablespace"] = check_tablespace(host, port, username, password, database, tablespace)

    return status
