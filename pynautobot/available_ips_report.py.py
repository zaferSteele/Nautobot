"""This script connects to a Nautobot instance and retrieves all /24 IP prefixes for the 'WayneHQ' location.
It prints each prefix, the number of available IP addresses in each, and the first available IP address if any."""

# Create a connection to the Nautobot API
# Replace the URL and token with your own Nautobot instance details
import pynautobot  # Import the pynautobot library to interact with the Nautobot API

# Create a connection to the Nautobot API
# Replace the URL and token with your own Nautobot instance details
nautobot = pynautobot.api(
    url="http://192.168.4.2:8001",  # URL of the Nautobot instance (This is just an example)
    token="014239586a4barc446774c4cdaj5gc0bc6f9f78f", # Personal API token for authentication (This is just an example)
    api_version="2.1"  # Specify the API version
)

# Query Nautobot for all prefixes with /24 subnet mask located at "WayneHQ", replace with your own location here
wayne_prefixes = nautobot.ipam.prefixes.filter(location="WayneHQ", prefix_length="24")

# Print a header and list all the /24 prefixes found for WayneHQ
print("\nWayneHQ has the following available Prefixes:")
print("-" * 45)
for prefix in wayne_prefixes:
    print(prefix)  # Print the full details of each prefix

# Print the number of available IP addresses in each prefix
print("\nNumber of IP addresses available for each WayneHQ prefix:")
print("-" * 45)
for prefix in wayne_prefixes:
    available_ips = prefix.available_ips.list()  # Get a list of available IPs in this prefix
    print(f"{prefix} has: {len(available_ips)} IP addresses available for use")  # Show count

# Print the first available IP address from each prefix (if any are available)
print("\nFirst available IP address from each WayneHQ prefix:")
print("-" * 45)
for prefix in wayne_prefixes:
    available_ips = prefix.available_ips.list()  # Re-fetch available IPs for this prefix
    if available_ips:
        first_ip = available_ips[0]  # Get the first available IP
        print(f"{prefix} -> {first_ip}")  # Print the first available IP
    else:
        print(f"{prefix} -> No available IPs")  # Handle the case where there are none
