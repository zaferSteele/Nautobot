# This script fetches all devices from a specific site using a location UUID,
# then prints all IP addresses assigned to each device at that site using the NetBox API.

import requests
import json

# Headers include authorization and content type for API access
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # replace this with your api token generated in Nautobot
}

# Starting API URL: get all devices at the given site (using location UUID)
devices_url = "http://<ip_address_of_your_nautobot_server>/api/dcim/devices/?location=<UUID>"
# Example : http://192.168.255.4:8001/api/dcim/devices/?location=1d6b4c31-e809-4702-bd0f-3b63a81e92a0



# Create a session to reuse the connection and automatically send headers
session = requests.session()
session.headers.update(headers)

# List to store all devices found at this location
all_devices = []

# Loop through paginated device list until there are no more pages
while devices_url is not None:
    response = session.get(devices_url)  # Request device list
    devices_url = response.json()["next"]  # Get URL for next page (or None if done)
    all_devices.extend(response.json()["results"])  # Add current page's devices to the list

# Loop through each device found at the location
for device in all_devices:
    # Create a new field/key to store this device's IPs
    device["our_interfaces"] = []

    # Build URL to get IP addresses for this specific device (by name)
    ip_url = f"http://<ip_address_of_your_nautobot_server>/api/ipam/ip-addresses?device={device['name']}"
    # Example : http://192.168.255.4:8001/api/ipam/ip-addresses?device={device['name']}

    # Fetch all IP addresses assigned to this device (with pagination)
    while ip_url is not None:
        ip_url_response = session.get(ip_url)  # Request IPs
        ip_url = ip_url_response.json()["next"]  # URL for next page (if any)
        device["our_interfaces"].extend(ip_url_response.json()["results"])  # Add IPs to list

    # Print each IP address assigned to this device
    for interface in device["our_interfaces"]:
        print(f"Device: {device['name']} has an IP Address {interface['address']}")
