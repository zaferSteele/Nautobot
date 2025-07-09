# This script sends a GraphQL query to an  The Nautobot GraphQL API to retrieve and print all devices located in "London".
# It authenticates using a token, constructs the query, and displays each device's name and location.

# Import necessary libraries
import requests  # allows sending HTTP requests
import json      # helps format data to and from JSON

# Create an empty dictionary to hold our request data
payload = {}

# Set up the headers for the HTTP request
headers = {
    "Content-Type": "application/json",     # tells the server we're sending JSON
    "Accept": "application/json",           # tells the server we want JSON back
    "Authorization": "Token 014239586a4ba1c446774thfgdcda4fde0bc6f9f78f",  # token to access the API (exmaple, use your own api token here)
}

# Start a new session object to reuse the same settings across requests
session = requests.Session()

# Add our headers to this session
session.headers.update(headers)

# Define the URL for the GraphQL API we're going to send the request to
graphql_url = "http://192.168.255.5:8001/api/graphql/" #example ip address of GraphQL API, , replace with your own Natuobot IP address here

# Write the GraphQL query to get devices located in "London" # can be replaced with any other location within your Nautobot instance
query = """
query {
    devices(location: "London"){
        name
        location{
         name   
        }
    }
}
"""

# Put the query into a dictionary as the payload
payload = {"query": query}

# Send the POST request to the API with our payload (convert it to JSON format)
r = session.post(graphql_url, data=json.dumps(payload))

# Optional: you can print the full response data to see what you get
# print(r.json())

# Loop through each device in the response and print its name and location
for device in r.json()['data']['devices']:
    print(f"Device: {device['name']} is in Location {device['location']['name']}")
