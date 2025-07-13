""" This script queries a Nautobot instance using GraphQL to retrieve device names
 and their location, filtered by a specific location ("London" in this case).
Import the pynautobot library, which allows Python to interact with a Nautobot API 
"""

import pynautobot

# Create a connection to the Nautobot API
# Replace the URL and token with your own Nautobot instance details
nautobot = pynautobot.api(
    url="http://192.168.4.2:8001",  # URL of the Nautobot instance (This is just an example)
    token="014239586a4ba1c446774c4cda45dc0bc6f9f78f",  # Personal API token for authentication (This is just an example)
    api_version="2.1"  # Specify the Nautobot API version to use
)

# Define a GraphQL query with a variable ($nautobot_location)
# The query will return device names and their location name, filtered by location
query = """
query($nautobot_location: [String]) {
    devices(location: $nautobot_location) {
        name  # The name of the device
        location {
            name  # The name of the location each device belongs to
        }
    }   
}
"""

# Define the value for the GraphQL variable in a dictionary
# Here, we're searching for devices at the location "London"
variables = {"nautobot_location": "London"}

# Send the GraphQL query along with the variables to the Nautobot server
response = nautobot.graphql.query(query=query, variables=variables)

# Print the HTTP status code of the response (e.g. 200 for success)
print(response.status_code)

# Print the data returned by Nautobot in JSON format
print(response.json)
