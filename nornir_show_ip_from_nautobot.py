# This script connects to a list of network devices using info pulled from the dynamic inventory.
# It sends the command "show ip int br" to each device using Nornir and Netmiko.
# The output of each device is printed to the screen.
# This is useful for checking interface status (IP address, status, protocol) across all devices.

# Import Nornir and plugins
from nornir import InitNornir
from nornir.core.inventory import Inventory, Host, Group  # Needed to build custom inventory
from nornir_netmiko.tasks import netmiko_send_command     # Used to send CLI commands to network devices
from inventory_loader import get_inventory                # This gets the inventory from Nautobot using inventory_loader.py 

from typing import List  # Helps describe types like lists


def load_inventory():
    # Get inventory data (devices, groups, etc.) from Nautobot
    inv_data = get_inventory()

    hosts = {}     # Will hold all device info
    groups = {}    # Will hold group (site) info
    defaults = inv_data.get("defaults", {})  # Default login info

    # First, create the group objects
    for groupname in inv_data.get("groups", {}):
        groups[groupname] = Group(name=groupname)

    # Now go through each device (host)
    for hostname, host_data in inv_data.get("hosts", {}).items():
        group_names: List[str] = host_data.get("groups", [])
        
        # Link group names to actual group objects
        host_groups = [groups[g] for g in group_names if g in groups]

        # Create a Host object with its IP, platform, login, and groups
        hosts[hostname] = Host(
            name=hostname,
            hostname=host_data["hostname"],        # IP address or hostname
            platform=host_data.get("platform", "ios"),  # e.g. ios, nxos
            groups=host_groups,
            username=defaults.get("username"),     # login username
            password=defaults.get("password"),     # login password
            data={},                               # extra data (empty for now)
        )

    # Return the full inventory for Nornir to use
    return Inventory(hosts=hosts, groups=groups, defaults=defaults)


def main():
    # Start Nornir without a config file
    nr = InitNornir(config_file=None)

    # Load our custom inventory from Nautobot
    nr.inventory = load_inventory()

    # Run the "show ip int br" command on every device
    results = nr.run(task=netmiko_send_command, command_string="show ip int br")

    # Show the command output for each device
    for host, result in results.items():
        print(f"\n{host} output:")
        print(result.result)


# Run the main() function if we are running this file directly
if __name__ == "__main__":
    main()
