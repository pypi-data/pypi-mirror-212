"""
ChocloChecker SOAP API Module

This module contains functions for checking the status of SOAP APIs.
"""

from zeep import Client, Transport

def check_status(url, operation_name):
    """
    Check the status of a SOAP API operation.

    Args:
        url (str): The URL of the SOAP API endpoint.
        operation_name (str): The name of the operation to check.

    Returns:
        str: The status of the SOAP API operation.
    """
    try:
        transport = Transport(timeout=10)
        client = Client(url, transport=transport)
        operation = client.service.__getattr__(operation_name)
        result = operation()

        return "Operation executed successfully"
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to the API: {str(e)}"
    except Exception as e:
        return f"Failed to execute operation: {str(e)}"


def check_soap_api(url, operation_name):
    """
    Check the status of a SOAP API.

    Args:
        url (str): The URL of the SOAP API endpoint.
        operation_name (str): The name of the operation to check.

    Returns:
        dict: A dictionary containing the status of the SOAP API.
            The dictionary includes the connection status and the status of the specified operation.
    """
    status = {}

    status["connection"] = check_status(url, "")
    status["operation_status"] = check_status(url, operation_name)

    return status
