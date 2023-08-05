"""
ChocloChecker Redis Module

This module contains the functions for monitoring the status of Redis databases.
"""

import redis

def check_connection(host, port, password=None):
    """
    Check the connection to the Redis server.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        r = redis.Redis(host=host, port=port, password=password)
        r.ping()
        return True
    except redis.ConnectionError:
        return False

def check_status(host, port, password=None):
    """
    Check the status of the Redis database.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        str: The status of the Redis database.
    """
    connection_status = check_connection(host, port, password)
    if connection_status:
        return "Database is running and accessible"
    else:
        return "Cannot connect to the database"

def check_keys(host, port, password=None):
    """
    Check the number of keys in the Redis database.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        int: The number of keys in the Redis database.
    """
    try:
        r = redis.Redis(host=host, port=port, password=password)
        num_keys = r.dbsize()
        return num_keys
    except redis.ConnectionError:
        return -1

def check_memory(host, port, password=None):
    """
    Check the memory usage of the Redis server.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        dict: A dictionary containing the memory usage statistics of the Redis server.
            The dictionary includes values such as used memory, max memory, memory fragmentation, etc.
    """
    try:
        r = redis.Redis(host=host, port=port, password=password)
        info = r.info()

        memory_stats = {
            "used_memory": info["used_memory"],
            "max_memory": info["max_memory"],
            "fragmentation_ratio": info["mem_fragmentation_ratio"]
        }

        return memory_stats
    except redis.ConnectionError:
        return {}

def check_replication(host, port, password=None):
    """
    Check the replication status of a Redis cluster.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        str: The replication status of the Redis cluster.
    """
    try:
        r = redis.Redis(host=host, port=port, password=password)
        info = r.info()

        if info.get("role") == "master":
            connected_slaves = info.get("connected_slaves")
            if connected_slaves > 0:
                return f"Replication is active with {connected_slaves} slave(s)"
            else:
                return "Replication is active"
        elif info.get("role") == "slave":
            master_host = info.get("master_host")
            master_port = info.get("master_port")
            return f"Connected to master at {master_host}:{master_port}"
        else:
            return "Replication is not configured"
    except redis.ConnectionError:
        return "Cannot connect to the server"

def check_redis(host, port, password=None):
    """
    Check the status of a Redis database.

    Args:
        host (str): The host address of the Redis server.
        port (int): The port number of the Redis server.
        password (str, optional): The password for Redis authentication.

    Returns:
        dict: A dictionary containing the status of the Redis database.
            The dictionary includes the connection status, database status, number of keys,
            memory usage statistics, replication status, and Redis version.
    """
    status = {}

    status["connection"] = check_connection(host, port, password)
    status["database"] = check_status(host, port, password)
    status["keys"] = check_keys(host, port, password)
    status["memory"] = check_memory(host, port, password)
    status["replication"] = check_replication(host, port, password)
    status["version"] = redis.__version__

    return status
