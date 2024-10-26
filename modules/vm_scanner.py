from os import environ
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

'''
https://learn.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.computemanagementclient?view=azure-python#azure-mgmt-compute-computemanagementclient-virtual-machines
'''

# Class VirtualMachineScanner


# Class VirtualMachine ScaleSet Scanner

class VirtualMachineScanner:
    def __init__(self, subscription_id:str = None):
        self.subscription_id = subscription_id
        self.cmc_client = self.setup_compute_client(subscription_id)

    def setup_compute_client(self, subscription_id:str) -> ComputeManagementClient:
        """Sets up the Authorization Management Client using DefaultAzureCredential."""
        try:
            cmc_client = ComputeManagementClient(
                DefaultAzureCredential(),
                self.subscription_id
            )
            return cmc_client
        except Exception as e:
            print(f"Failed to create AuthorizationManagementClient: {e}")
            return None
    
    def list_all_vms(self):
        return self.cmc_client.virtual_machines.list_all()


class VirtualMachineScaleSetScanner(ComputeManagementClient):
    pass


vm_client = VirtualMachineScanner(subscription_id=environ['AZURE_SUBSCRIPTION_ID'])
for vm in vm_client.list_all_vms():
    print(vm)