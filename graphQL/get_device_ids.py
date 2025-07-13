"""This script connects to a Nautobot instance and sends a simple GraphQL query
    to retrieve the IDs of all devices in the system, then prints the result.
"""

# Import the pynautobot library, which allows Python to interact with a Nautobot API
import pynautobot

# Create a connection to the Nautobot API
# Replace the URL and token with your own Nautobot instance details
nautobot = pynautobot.api(
    url="http://192.168.4.2:8001",  # URL of the Nautobot instance (This is just an example)
    token="014239586a4ba1c4jk74c4cda45dc0bc6f9f78f",  # Personal API token for authentication (This is just an example)
    api_version="2.1"  # Specify the Nautobot API version to use
)

# Define a GraphQL query as a multi-line string
# This query is asking Nautobot to return a list of devices and their IDs
query = """
query {
    devices {
        id  # This tells Nautobot to only return the ID of each device
    }
}
"""

# Send the GraphQL query to Nautobot and store the response
response = nautobot.graphql.query(query=query)

# Print the JSON-formatted response from Nautobot
print(response.json)
