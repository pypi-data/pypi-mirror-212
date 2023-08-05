"""
ChocloChecker MongoDB Module

This module contains the functions for monitoring the status of MongoDB databases.
"""

import pymongo
from pymongo.errors import ConnectionFailure
def check_connection(host, port):
    """
    Check the connection to the MongoDB server.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        client = pymongo.MongoClient(host, port)
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        return False

def check_status(host, port):
    """
    Check the status of the MongoDB database.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        str: The status of the MongoDB database.
    """
    connection_status = check_connection(host, port)
    if connection_status:
        # Perform other status checks
        # ...

        return "Database is running and accessible"
    else:
        return "Cannot connect to the database"


def check_collections(host, port, collections):
    """
    Check the existence of specific collections in the MongoDB database.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.
        collections (list): A list of collection names to check.

    Returns:
        list: A list of dictionaries representing the existence status of each collection.
            Each dictionary contains the collection name and a boolean value indicating its existence.
    """
    try:
        client = pymongo.MongoClient(host, port)
        db = client.get_database()
        existing_collections = db.list_collection_names()

        collection_status = []
        for collection in collections:
            status = {
                "collection": collection,
                "exists": collection in existing_collections
            }
            collection_status.append(status)

        return collection_status
    except pymongo.errors.ConnectionError:
        return []

def check_replication(host, port):
    """
    Check the replication status of a MongoDB cluster.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        str: The replication status of the MongoDB cluster.
    """
    try:
        client = pymongo.MongoClient(host, port)
        repl_status = client.admin.command('replSetGetStatus')

        if repl_status:
            return "Replication is active"
        else:
            return "Replication is not configured"
    except pymongo.errors.ConnectionError:
        return "Cannot connect to the server"

def check_capacity(host, port):
    """
    Check the capacity and usage statistics of the MongoDB server.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        dict: A dictionary containing capacity and usage statistics of the MongoDB server.
            The dictionary includes values such as total storage, free storage, memory usage, etc.
    """
    try:
        client = pymongo.MongoClient(host, port)
        server_status = client.admin.command('serverStatus')

        capacity_stats = {
            "storage": {
                "total": server_status["storageSize"],
                "free": server_status["storageSize"] - server_status["dataSize"]
            },
            "memory": {
                "total": server_status["mem"]["totalVirtual"],
                "used": server_status["mem"]["virtual"]
            }
        }

        return capacity_stats
    except pymongo.errors.ConnectionError:
        return {}

def check_security(host, port):
    """
    Check the security settings and configurations of the MongoDB server.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        dict: A dictionary containing the security settings and configurations of the MongoDB server.
            The dictionary includes values such as authentication enabled, SSL/TLS enabled, etc.
    """
    try:
        client = pymongo.MongoClient(host, port)
        server_status = client.admin.command('serverStatus')

        security_settings = {
            "authentication": server_status["security"]["authenticationEnabled"],
            "ssl": server_status["security"]["SSLServerSubjectName"]
        }

        return security_settings
    except pymongo.errors.ConnectionError:
        return {}

def check_version(host, port):
    """
    Check the version of the MongoDB server.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.

    Returns:
        str: The version of the MongoDB server.
    """
    try:
        client = pymongo.MongoClient(host, port)
        server_info = client.server_info()
        version = server_info['version']
        return version
    except pymongo.errors.ConnectionError:
        return "Cannot connect to the server"

def check_mongodb(host, port, collections):
    """
    Check the status of a MongoDB database.

    Args:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.
        collections (list): A list of collection names to check.

    Returns:
        dict: A dictionary containing the status of the MongoDB database.
            The dictionary includes the connection status, database status, collection status,
            replication status, capacity statistics, security settings, and MongoDB version.
    """
    status = {}

    status["connection"] = check_connection(host, port)
    status["database"] = check_status(host, port)
    status["collections"] = check_collections(host, port, collections)
    status["replication"] = check_replication(host, port)
    status["capacity"] = check_capacity(host, port)
    status["security"] = check_security(host, port)
    status["version"] = check_version(host, port)

    return status
