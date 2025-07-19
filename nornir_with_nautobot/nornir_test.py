"""This script connects to a Nautobot inventory using Nornir, filters hosts by location,
and runs a simple test task on each host to verify automation connectivity and output. """

#######################################################################################################
#REQUIREMENTS:
#Installation of nornir-nautobot: "pip install nornir-nautobot"
#Make sure you run these commands in your shell, the following URL and Token are just examples:
#   export NAUTOBOT_URL=http://192.168.5.1:8001
#   export NAUTOBOT_TOKEN=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
#######################################################################################################

import os # Used to access environment variables in this case the NAUTOBOT URL and its API TOKEN
from nornir import InitNornir # Main function to initialize Nornir with an inventory
from nornir.core.task import Task, Result # Base classes to define tasks and their results
from nornir_utils.plugins.functions import print_result # Norninr Utility to print task results in a readable format


# This function defines a simple task that Nornir will run on each host, this is for testing purposes.
# It buiild a Result object with a custom message for each host.
def print_automate(task):
    return Result(host=task.host, result=f"{task.host.name} says I can be automated!")

# The main function initialises the Nornir environment
def main():
    # List of locations we want to filter hosts by (this can be changed)
    locations = ["London"]
    
    # Initialise Nornir, the Inventory plugin "NautobotInventory" will be used to retrieve hosts from Nautobot
    # Credentials (URL and token) are extracted from environment variables for security
    
    test_nornir = InitNornir(
        inventory={
            "plugin": "NautobotInventory", # Use Nautobot as the source of the host inventory
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"), # URL of the Nautobot server
                "nautobot_token": os.getenv("NAUTOBOT_TOKEN"), # Auth token for Nautobot
                "filter_parameters": {"location": locations}, # Only include hosts from these locations
                "ssl_verify": True, # Ensure SSL certificiate is verfied for security
            },
        },
    )

    # Show how many hosts were found in the inventory
    print(f"Hosts found: {len(test_nornir.inventory.hosts)}")
    # Show the names of the hosts within the inventory
    print(test_nornir.inventory.hosts.keys())
    # Run the print_automate task on all the hosts 
    result = test_nornir.run(task=print_automate)
    # Nicely show the results from each host
    print_result(result)

# Ensures main() runs only if the script is excecuted directly.
if __name__ == "__main__":
    main()