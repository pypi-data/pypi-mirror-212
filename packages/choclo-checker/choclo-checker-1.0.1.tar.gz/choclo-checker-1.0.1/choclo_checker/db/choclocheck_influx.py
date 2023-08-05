"""
ChocloChecker InfluxDB Module

This module contains the functions for monitoring the status of InfluxDB databases.
"""

from influxdb import InfluxDBClient

def check_connection(host, port, username=None, password=None, database=None):
    """
    Check the connection to the InfluxDB server.

    Args:
        host (str): The host address of the InfluxDB server.
        port (int): The port number of the InfluxDB server.
        username (str, optional): The username for InfluxDB authentication.
        password (str, optional): The password for InfluxDB authentication.
        database (str, optional): The name of the InfluxDB database.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
        databases = client.get_list_database()
        return True
    except Exception:
        return False

def check_status(host, port, username=None, password=None, database=None):
    """
    Check the status of the InfluxDB database.

    Args:
        host (str): The host address of the InfluxDB server.
        port (int): The port number of the InfluxDB server.
        username (str, optional): The username for InfluxDB authentication.
        password (str, optional): The password for InfluxDB authentication.
        database (str, optional): The name of the InfluxDB database.

    Returns:
        str: The status of the InfluxDB database.
    """
    connection_status = check_connection(host, port, username, password, database)
    if connection_status:
        return "Database is running and accessible"
    else:
        return "Cannot connect to the database"

def check_measurement(host, port, username=None, password=None, database=None, measurement=None):
    """
    Check the data points of a specific measurement in the InfluxDB database.

    Args:
        host (str): The host address of the InfluxDB server.
        port (int): The port number of the InfluxDB server.
        username (str, optional): The username for InfluxDB authentication.
        password (str, optional): The password for InfluxDB authentication.
        database (str, optional): The name of the InfluxDB database.
        measurement (str, optional): The name of the measurement to check.

    Returns:
        dict: A dictionary containing the data points of the specified measurement.
    """
    try:
        client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
        query = f"SELECT * FROM {measurement}"
        result = client.query(query)
        data_points = list(result.get_points())
        return data_points
    except Exception:
        return []

def check_influxdb(host, port, username=None, password=None, database=None, measurement=None):
    """
    Check the status of an InfluxDB database.

    Args:
        host (str): The host address of the InfluxDB server.
        port (int): The port number of the InfluxDB server.
        username (str, optional): The username for InfluxDB authentication.
        password (str, optional): The password for InfluxDB authentication.
        database (str, optional): The name of the InfluxDB database.
        measurement (str, optional): The name of the measurement to check.

    Returns:
        dict: A dictionary containing the status of the InfluxDB database.
            The dictionary includes the connection status, database status, and
            the data points of the specified measurement.
    """
    status = {}

    status["connection"] = check_connection(host, port, username, password, database)
    status["database"] = check_status(host, port, username, password, database)
    if measurement:
        status["measurement"] = check_measurement(host, port, username, password, database, measurement)

    return status
