"""
ChocloChecker REST API Module

This module contains functions for checking the status of REST APIs.
"""

import requests

def check_status(url):
    """
    Check the status of a REST API endpoint.

    Args:
        url (str): The URL of the API endpoint.

    Returns:
        str: The status of the API endpoint.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return "API is up and running"
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to the API: {str(e)}"
    except requests.exceptions.HTTPError as e:
        return f"API returned status code {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def check_rest_api(url):
    """
    Check the status of a REST API.

    Args:
        url (str): The base URL of the REST API.

    Returns:
        dict: A dictionary containing the status of the REST API.
            The dictionary includes the connection status and the status of the API endpoint.
    """
    status = {}

    status["connection"] = check_status(url)
    status["api_status"] = check_status(url + "/status")

    return status
