"""
ChocloChecker Oracle Module

This module contains the functions for monitoring the status of Oracle databases.
"""

import cx_Oracle

def check_connection(host, port, username, password, service_name):
    """
    Check the connection to the Oracle database.

    Args:
        host (str): The host address of the Oracle server.
        port (int): The port number of the Oracle server.
        username (str): The username for Oracle authentication.
        password (str): The password for Oracle authentication.
        service_name (str): The name of the Oracle service.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        connection = cx_Oracle.connect(username, password, dsn)
        connection.close()
        return True
    except cx_Oracle.DatabaseError:
        return False

def check_status(host, port, username, password, service_name):
    """
    Check the status of the Oracle database.

    Args:
        host (str): The host address of the Oracle server.
        port (int): The port number of the Oracle server.
        username (str): The username for Oracle authentication.
        password (str): The password for Oracle authentication.
        service_name (str): The name of the Oracle service.

    Returns:
        str: The status of the Oracle database.
    """
    connection_status = check_connection(host, port, username, password, service_name)
    if connection_status:
        return "Database is running and accessible"
    else:
        return "Cannot connect to the database"

def check_tablespace(host, port, username, password, service_name, tablespace):
    """
    Check the status of a specific tablespace in the Oracle database.

    Args:
        host (str): The host address of the Oracle server.
        port (int): The port number of the Oracle server.
        username (str): The username for Oracle authentication.
        password (str): The password for Oracle authentication.
        service_name (str): The name of the Oracle service.
        tablespace (str): The name of the tablespace to check.

    Returns:
        dict: A dictionary containing the status of the specified tablespace.
            The dictionary includes values such as total space, used space, and free space.
    """
    try:
        dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()

        query = f"SELECT tablespace_name, round(SUM(bytes)/1024/1024, 2) total_space, " \
                f"round(SUM(bytes - decode(maxbytes, 0, bytes))/1024/1024, 2) used_space, " \
                f"round(SUM(decode(maxbytes, 0, bytes))/1024/1024, 2) free_space " \
                f"FROM dba_data_files WHERE tablespace_name = '{tablespace}' " \
                f"GROUP BY tablespace_name"
        cursor.execute(query)
        result = cursor.fetchone()

        tablespace_status = {
            "tablespace": result[0],
            "total_space": result[1],
            "used_space": result[2],
            "free_space": result[3]
        }

        cursor.close()
        connection.close()

        return tablespace_status
    except cx_Oracle.DatabaseError:
        return {}

def check_oracle(host, port, username, password, service_name, tablespace=None):
    """
    Check the status of an Oracle database.

    Args:
        host (str): The host address of the Oracle server.
        port (int): The port number of the Oracle server.
        username (str): The username for Oracle authentication.
        password (str): The password for Oracle authentication.
        service_name (str): The name of the Oracle service.
        tablespace (str, optional): The name of the tablespace to check.

    Returns:
        dict: A dictionary containing the status of the Oracle database.
            The dictionary includes the connection status, database status,
            and the status of the specified tablespace (if provided).
    """
    status = {}

    status["connection"] = check_connection(host, port, username, password, service_name)
    status["database"] = check_status(host, port, username, password, service_name)
    if tablespace:
        status["tablespace"] = check_tablespace(host, port, username, password, service_name, tablespace)

    return status
