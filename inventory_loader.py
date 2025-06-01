# This python script dynamically creates an inventory dictionary for use with the Nornir framework
# It retrieves device and IP address information from a Nautobot server via its REST API.

import requests  # For making HTTP requests to the Nautobot API
import json      # For formatting output and handling JSON data

# Base URL of your Nautobot instance — replace with your own server address
NAUTOBOT_URL = "http://192.168.255.2:8001"

# Your personal Nautobot API token
NAUTOBOT_TOKEN = "014239586a4ba1c446774c4cda45dc0bc6f9f78f"

# HTTP headers for authentication and content negotiation
HEADERS = {
    "Authorization": f"Token {NAUTOBOT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_ip_address(ip_obj):
    """
    Given a dictionary containing a 'url' to an IP address object in Nautobot,
    fetch the full address and return just the IP part (strip subnet mask).
    """
    if not ip_obj or not isinstance(ip_obj, dict):
        return None  # Return nothing if the input is invalid

    ip_url = ip_obj.get("url")
    if not ip_url:
        return None

    # Handle relative URLs by prefixing with base Nautobot URL
    full_url = ip_url if ip_url.startswith("http") else f"{NAUTOBOT_URL}{ip_url}"

    try:
        # Send a GET request to retrieve the full IP address object
        response = requests.get(full_url, headers=HEADERS)
        response.raise_for_status()  # Raise error if response is not 200 OK
        data = response.json()
        # Extract just the IP (before the / subnet)
        return data.get("address", "").split("/")[0]
    except Exception as e:
        print(f" Failed to get IP from {full_url}: {e}")
        return None


def get_inventory():
    """
    Builds an inventory dictionary using device data from Nautobot.
    Each host includes its IP, platform type, and group based on site.
    """
    # API URL to fetch all devices (limit=0 = no pagination)
    devices_url = f"{NAUTOBOT_URL}/api/dcim/devices/?limit=0"

    # Request device data from Nautobot
    response = requests.get(devices_url, headers=HEADERS)
    response.raise_for_status()
    devices = response.json()["results"]

    # Start building the inventory structure
    inventory = {
        "hosts": {},   # Will store device-specific info
        "groups": {},  # Will store group/site-level info
        "defaults": {  # Default credentials for all devices
            "username": "admin",
            "password": "cisco"
        }
    }

    # Loop through each device returned from Nautobot
    for device in devices:
        name = device["name"]  # Device name

        # Get primary IPv4 or fallback to any IP (depends on Nautobot version)
        ip_obj = device.get("primary_ip4") or device.get("primary_ip")
        ip_address = get_ip_address(ip_obj)

        if not ip_address:
            print(f" Device '{name}' has no usable primary IP. Skipping.")
            continue  # Skip devices without a usable IP

        # Get platform (e.g., ios, nxos, etc.)
        platform = device.get("platform") or {}
        platform_slug = platform.get("slug", "ios")  # Default to 'ios'

        # Use site slug as group name
        site = device.get("site") or {}
        site_slug = site.get("slug", "default")

        # Add this device to the hosts dictionary
        inventory["hosts"][name] = {
            "hostname": ip_address,
            "platform": platform_slug,
            "groups": [site_slug],  # Grouped by site
        }

        # Ensure the group exists in the inventory
        if site_slug not in inventory["groups"]:
            inventory["groups"][site_slug] = {}

    # Optionally print out the entire inventory
    print("Inventory has been generated")

    # Create a new dictionary that is the same as inventory, but without the "defaults" key
    # This is used just for printing, so we don’t show login info
    printable_inventory = {k: v for k, v in inventory.items() if k != "defaults"}

    # Print the cleaned-up inventory in a nice readable format (with indentation)
    print(json.dumps(printable_inventory, indent=4))


    return inventory


# This runs the function if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    get_inventory()
