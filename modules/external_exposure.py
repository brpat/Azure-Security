from os import environ
from azure.mgmt.network import NetworkManagementClient
from azure.identity import DefaultAzureCredential


'''
https://learn.microsoft.com/en-us/python/api/overview/azure/network?view=azure-python
https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network?view=azure-python
https://learn.microsoft.com/en-us/python/api/azure-mgmt-networkcloud/azure.mgmt.networkcloud.networkcloudmgmtclient?view=azure-python
'''

class PublicExposureScanner:
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(), 
            subscription_id=subscription_id
        )

    def enumerate_vnets(self, name_only=True) -> list:
        """
            Enumerate all Virtual Networks in the subscription. 
            Set name_only to False to return full vnet object
        """

        vnets = self.network_client.virtual_networks.list_all()

        return [vnet.name if name_only else vnet for vnet in vnets]


    def enumerate_nics(self):
        """Enumerate all Network Interface Cards (NICs) in the subscription."""
        nics = self.network_client.network_interfaces.list_all()
        nic_list = []
        for nic in nics:
            nic_list.append({
                "nic_name": nic.name,
                "resource_group": nic.id.split('/')[4],  # Extract the resource group from the ID
                "ip_configurations": nic.ip_configurations
            })
        return nic_list

    def check_public_ip(self, resource_group_name, public_ip_name):
        """Check details of a Public IP."""
        public_ip = self.network_client.public_ip_addresses.get(
            resource_group_name, public_ip_name
        )
        if public_ip:
            return {
                "ip_address": public_ip.ip_address,
                "allocation_method": public_ip.public_ip_allocation_method,
                "is_static": public_ip.public_ip_allocation_method == 'Static'
            }
        return None

    def check_nsg_rules(self, resource_group_name, nsg_name):
        """Check NSG rules for a Network Security Group."""
        nsg_rules = self.network_client.security_rules.list(resource_group_name, nsg_name)
        exposed_rules = []
        for rule in nsg_rules:
            if rule.access == 'Allow' and rule.destination_address_prefix == '0.0.0.0/0':
                exposed_rules.append({
                    "rule_name": rule.name,
                    "protocol": rule.protocol,
                    "ports": rule.destination_port_ranges,
                    "direction": rule.direction
                })
        return exposed_rules

    def enumerate_load_balancers(self):
        """Enumerate all Load Balancers and check if any are public-facing."""
        load_balancers = self.network_client.load_balancers.list_all()
        lb_list = []
        for lb in load_balancers:
            for frontend_ip_config in lb.frontend_ip_configurations:
                if frontend_ip_config.public_ip_address:
                    public_ip_name = frontend_ip_config.public_ip_address.id.split('/')[-1]
                    resource_group = frontend_ip_config.public_ip_address.id.split('/')[4]
                    public_ip_details = self.check_public_ip(resource_group, public_ip_name)
                    lb_list.append({
                        "lb_name": lb.name,
                        "public_ip": public_ip_details
                    })
        return lb_list

    def find_public_exposures(self):
        """Find all resources with public exposure."""
        public_exposures = []

        # Step 1: Enumerate NICs
        nics = self.enumerate_nics()
        for nic in nics:
            resource_group = nic['resource_group']
            for ip_config in nic['ip_configurations']:
                if ip_config.public_ip_address:
                    public_ip_name = ip_config.public_ip_address.id.split('/')[-1]
                    public_ip_details = self.check_public_ip(resource_group, public_ip_name)

                    if public_ip_details:
                        # Step 2: Check NSG Rules
                        if nic.network_security_group:
                            nsg_name = nic.network_security_group.id.split('/')[-1]
                            exposed_nsg_rules = self.check_nsg_rules(resource_group, nsg_name)

                            if exposed_nsg_rules:
                                public_exposures.append({
                                    "nic_name": nic['nic_name'],
                                    "public_ip": public_ip_details,
                                    "exposed_ports": [rule['ports'] for rule in exposed_nsg_rules]
                                })

        # Step 3: Check Load Balancers
        load_balancers = self.enumerate_load_balancers()
        if load_balancers:
            public_exposures.extend(load_balancers)

        return public_exposures


scanner = PublicExposureScanner(subscription_id=environ['AZURE_SUBSCRIPTION_ID'])
print(scanner.enumerate_vnets(name_only=True))