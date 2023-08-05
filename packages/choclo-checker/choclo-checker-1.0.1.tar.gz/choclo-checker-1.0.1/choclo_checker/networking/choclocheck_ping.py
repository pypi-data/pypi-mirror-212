"""
ChocloChecker Ping Module

This module contains functions for checking network connectivity using ping.
"""

import platform
import subprocess

def check_connectivity(host):
    """
    Check the network connectivity to a host using ping.

    Args:
        host (str): The IP address or hostname to ping.

    Returns:
        bool: True if the host is reachable, False otherwise.
    """
    operating_system = platform.system().lower()
    if operating_system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", host]
    else:
        command = ["ping", "-c", "1", "-W", "1", host]

    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True)
        output = result.stdout.lower()
        if "unreachable" in output or "host unreachable" in output:
            return False
        return True
    except subprocess.CalledProcessError:
        return False


def check_ping(host):
    """
    Check the status of network connectivity to a host.

    Args:
        host (str): The IP address or hostname to check.

    Returns:
        dict: A dictionary containing the status of network connectivity.
            The dictionary includes the host name, IP address, and the connectivity status.
    """
    status = {}

    status["host"] = host
    status["ip_address"] = get_ip_address(host)
    status["connectivity"] = check_connectivity(host)

    return status


def get_ip_address(host):
    """
    Get the IP address of a host.

    Args:
        host (str): The hostname to resolve.

    Returns:
        str: The IP address of the host.
    """
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return None
