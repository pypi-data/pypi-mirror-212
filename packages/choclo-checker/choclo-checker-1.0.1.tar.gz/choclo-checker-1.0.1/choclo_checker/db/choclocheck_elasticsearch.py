"""
ChocloChecker Elasticsearch Module

This module contains the functions for monitoring the status of Elasticsearch clusters.
"""

from elasticsearch import Elasticsearch

def check_connection(hosts):
    """
    Check the connection to the Elasticsearch cluster.

    Args:
        hosts (list): A list of Elasticsearch host addresses.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        es = Elasticsearch(hosts)
        return es.ping()
    except:
        return False

def check_cluster_health(hosts):
    """
    Check the health status of the Elasticsearch cluster.

    Args:
        hosts (list): A list of Elasticsearch host addresses.

    Returns:
        str: The health status of the Elasticsearch cluster.
    """
    try:
        es = Elasticsearch(hosts)
        health = es.cluster.health()
        return health["status"]
    except:
        return "Unknown"

def check_indices(hosts):
    """
    Check the status of all indices in the Elasticsearch cluster.

    Args:
        hosts (list): A list of Elasticsearch host addresses.

    Returns:
        dict: A dictionary containing the status of all indices in the cluster.
            The dictionary includes the index name, document count, and size.
    """
    try:
        es = Elasticsearch(hosts)
        indices = es.indices.stats()
        index_status = {}

        for index_name, index_stats in indices["indices"].items():
            index_status[index_name] = {
                "document_count": index_stats["total"]["docs"]["count"],
                "size": index_stats["total"]["store"]["size"]
            }

        return index_status
    except:
        return {}

def check_elasticsearch(hosts):
    """
    Check the status of the Elasticsearch cluster.

    Args:
        hosts (list): A list of Elasticsearch host addresses.

    Returns:
        dict: A dictionary containing the status of the Elasticsearch cluster.
            The dictionary includes the connection status, cluster health status,
            and the status of all indices in the cluster.
    """
    status = {}

    status["connection"] = check_connection(hosts)
    status["cluster_health"] = check_cluster_health(hosts)
    status["indices"] = check_indices(hosts)

    return status
