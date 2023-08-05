"""
ChocloChecker GraphQL API Module

This module contains functions for checking the status of GraphQL APIs.
"""

import requests
from graphqlclient import GraphQLClient

def check_status(url, query):
    """
    Check the status of a GraphQL API.

    Args:
        url (str): The URL of the GraphQL API endpoint.
        query (str): The GraphQL query to execute.

    Returns:
        str: The status of the GraphQL API.
    """
    try:
        client = GraphQLClient(url)
        result = client.execute(query)

        return "API is up and running"
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to the API: {str(e)}"
    except Exception as e:
        return f"Failed to execute GraphQL query: {str(e)}"


def check_graphql_api(url, query):
    """
    Check the status of a GraphQL API.

    Args:
        url (str): The URL of the GraphQL API endpoint.
        query (str): The GraphQL query to execute.

    Returns:
        dict: A dictionary containing the status of the GraphQL API.
            The dictionary includes the connection status and the status of the API endpoint.
    """
    status = {}

    status["connection"] = check_status(url, query)

    return status
