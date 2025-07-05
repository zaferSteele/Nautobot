# This script automates the creation of a device in Nautobot, adds a Loopback0 interface to it,
# assigns an IP address to that interface, and links the IP address to the interface using the Nautobot API.

import requests
import json

# Define the details for the new device, UUID can be found easily by looking at the URL for each of these sections in the Nautobotn GUI
payload = {
    "name": "Zafers_automated_device",                      # Name of the device to be created
    "device_type": "59f1bd67-c8a2-404f-a389-826f18b4722c",  # UUID of the device type
    "status": "19272abb-fbf0-4a6b-ab99-9e52ec65dd3e",       # UUID representing active status
    "role": "3187bbf1-10eb-438c-9e13-1ed1a1e0ac7b",          # UUID for the device role
    "tenant": "191b26d6-24c7-4d4f-a23e-06a6e1938bc9",        # UUID for tenant association
    "platform": "0044165b-fe28-4bb2-8f7b-f03bd0d1ea23",     # UUID for platform info
    "location": "1d6b4c31-e809-4702-bd0f-3b63a81e92a0"       # UUID for physical location
}

# Define HTTP headers including authorization token
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Token  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # replace this with your api token generated in Nautobot
}

# Create a session to reuse the connection and automatically send headers
session = requests.Session()
session.headers.update(headers)

# Endpoint to create the device
devices_url = "http://<ip_address_of_your_nautobot_server>/api/dcim/devices/"
# Example: "http://192.168.255.4:8001/api/dcim/devices/"

# Make the API request to create the device
r = session.post(devices_url, data=json.dumps(payload))

# Extract the UUID of the newly created device
device_id = r.json()["id"]

# Endpoint to create a new interface
interface_url = "http://<ip_address_of_your_nautobot_server>/api/dcim/interfaces/"
# Example: "http://192.168.255.4:8001/api/dcim/interfaces/"

# Payload for the new virtual interface named 'Loopback0'
payload = {
    "device": device_id,
    "name": "Loopback0",
    "status": "19272abb-fbf0-4a6b-ab99-9e52ec65dd3e",  # Use same active status UUID
    "type": "virtual"  # Indicates it's a virtual interface
}

# Create the interface and get its ID
r = session.post(interface_url, data=json.dumps(payload))
interface_id = r.json()["id"]

# Endpoint to create a new IP address
ip_address_url = "http://<ip_address_of_your_nautobot_server>/api/ipam/ip-addresses/"
# Example: "http://192.168.255.4:8001/api/ipam/ip-addresses/"


# Payload for the new IP address, make sure you have created a parent prefix/global prefix
# otherwise you will get an error of the ["id"] key not existing.
# for debug purposes use: print("Response:", response.json()) after the execution of the session.post() method

payload = {
    "address": "10.1.3.1/32",  # IP address with subnet
    "namespace": "e7c3661c-af83-4e1e-8427-1d7d6a7c1049",  # Namespace UUID
    "tenant": "191b26d6-24c7-4d4f-a23e-06a6e1938bc9",  # Reuse tenant UUID
    "type": "host",  # Type of address
    "status": "19272abb-fbf0-4a6b-ab99-9e52ec65dd3e",  # Active status
    "dns_name": "Zafers-automated-device.com",  # DNS record for this IP
}

# Create the IP address
r = session.post(ip_address_url, json=payload)

# Extract the ID of the new IP address
ipaddr_id = r.json()["id"]

# Endpoint to associate the IP address to the interface
ipam_url = "http://<ip_address_of_your_nautobot_server>/api/ipam/ip-address-to-interface/"
# Example: "http://192.168.255.4:8001/api/ipam/ip-address-to-interface/"


# Payload linking IP to interface
payload = {
    "interface": interface_id,
    "ip_address": ipaddr_id
}

# Perform the association
r = session.post(ipam_url, data=json.dumps(payload))
