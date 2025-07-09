# This script queries the Nautobot GraphQL API to retrieve and display device names and their locations.
# It uses a variable in the query to dynamically filter devices by a specified location (e.g. "London").

# Import necessary libraries
import requests  # for making HTTP requests
import json      # for converting Python objects to JSON and vice versa

# Create an empty payload dictionary (not needed yet, but declared for completeness)
payload = {}

# Define headers to include in the HTTP request
headers = {
    "Content-Type": "application/json",   # tells the server we're sending JSON data
    "Accept": "application/json",         # tells the server we expect JSON in response
    "Authorization": "Token 014239586a4ba1c4567h4c4hdf45dc0bc6f9f78f",  # token to access the API (exmaple, use your own api token here)
}

# Create a session to persist settings like headers across multiple requests
session = requests.Session()
session.headers.update(headers)  # Add headers to the session

# Set the URL for the GraphQL API endpoint
graphql_url = "http://192.168.255.5:8001/api/graphql/" #example ip address of GraphQL API, replace with your own Natuobot IP address here

# Define the GraphQL query with a variable for location
query = """query ($nautobot_location: [String]){
    devices(location: $nautobot_location) {
     name
     location{
       name
     }   
    }
}
"""

# Prepare the payload with the query and variables
# We're setting the variable $nautobot_location to "London", can be replaced to any location within your Nautobot instance
payload = {
    "query": query,
    "variables": {
        "nautobot_location": "London"   
    }
}

# Send a POST request to the GraphQL API with the query and variables
r = session.post(graphql_url, data=json.dumps(payload))

# Optional: print the entire response JSON to inspect it
# print(r.json())

# Loop through each device returned and print its name and location
for device in r.json()['data']['devices']:
    print(f"Device: {device['name']} is in Location {device['location']['name']}")
