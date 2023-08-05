"""
ChocloChecker DynamoDB Module

This module contains the functions for monitoring the status of DynamoDB tables.
"""

import boto3

def check_connection(region_name):
    """
    Check the connection to the DynamoDB service.

    Args:
        region_name (str): The AWS region name.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        dynamodb.meta.client.list_tables()
        return True
    except:
        return False

def check_table_status(region_name, table_name):
    """
    Check the status of a DynamoDB table.

    Args:
        region_name (str): The AWS region name.
        table_name (str): The name of the DynamoDB table.

    Returns:
        dict: A dictionary containing the status of the DynamoDB table.
            The dictionary includes values such as the table name, number
            of items, and provisioned throughput.
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        table = dynamodb.Table(table_name)

        table_status = {
            "table_name": table_name,
            "item_count": table.item_count,
            "provisioned_throughput": table.provisioned_throughput
        }

        return table_status
    except:
        return {}

def check_dynamodb(region_name, table_name=None):
    """
    Check the status of a DynamoDB table or the DynamoDB service.

    Args:
        region_name (str): The AWS region name.
        table_name (str, optional): The name of the DynamoDB table.

    Returns:
        dict: A dictionary containing the status of the DynamoDB table or
            the DynamoDB service. The dictionary includes the connection
            status and the status of the specified table (if provided).
    """
    status = {}

    status["connection"] = check_connection(region_name)
    if table_name:
        status["table"] = check_table_status(region_name, table_name)

    return status
