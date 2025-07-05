# This script runs a specific Nautobot job using the API.
# You must replace the <job name> in the URL and the API token with valid values.

import requests
import json

# Initial empty payload (can include job input parameters if required)
payload = {}

# Headers for the API request, including the authorization token
headers = {
    "Content-Type": "application/json",  # Sending JSON data
    "Accept": "application/json",        # Expecting JSON response
    "Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Replace with your Nautobot API token
}

# Create a session and apply the headers to all requests
session = requests.Session()
session.headers.update(headers)

# Payload containing the data to pass to the job; empty 'data' for jobs with no input
payload = {
    "data": {}
}

# URL to run the job; replace <job name> with the actual job name or full module path
run_job_url = "http://192.168.255.2:8001/api/extras/jobs/<job name>/run/"

# Send the POST request to execute the job
r = session.post(run_job_url, data=json.dumps(payload))

# Print the HTTP status code to verify success (200 = OK, 201 = Created, etc.)
print(r.status_code)
